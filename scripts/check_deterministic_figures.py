#!/usr/bin/env python3
"""Execute every committed figure notebook twice and compare same-runner PNG bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "figures" / "notebooks"
FIGURE_DIR = ROOT / "figures"
MANIFEST = ROOT / "provenance" / "release_artifact_manifest.json"


def hashes() -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(FIGURE_DIR.glob("*.png"))
    }


def execute_all(output_dir: Path) -> None:
    def execute(notebook: Path) -> None:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--execute",
                "--to",
                "notebook",
                f"--ExecutePreprocessor.timeout=120",
                f"--output-dir={output_dir}",
                f"--output={notebook.name}",
                notebook.name,
            ],
            cwd=NOTEBOOK_DIR,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    notebooks = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(execute, notebooks))


def main() -> None:
    expected = {
        Path(item["path"]).name: item["sha256"]
        for item in json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
        if item["path"].startswith("figures/") and item["path"].endswith(".png")
    }
    with tempfile.TemporaryDirectory(prefix="ethical-debt-notebooks-") as tmp:
        output = Path(tmp)
        execute_all(output)
        first = hashes()
        execute_all(output)
        second = hashes()
    if first != second:
        changed = sorted(name for name in set(first) | set(second) if first.get(name) != second.get(name))
        raise RuntimeError(f"Figure execution is not byte-stable: {', '.join(changed)}")
    if set(second) != set(expected):
        changed = sorted(set(second) ^ set(expected))
        raise RuntimeError(f"Regenerated figure set differs from the release contract: {', '.join(changed)}")
    print(
        f"Deterministic figure execution passed: {len(second)} PNG files, "
        "two byte-identical executions on this runner."
    )


if __name__ == "__main__":
    main()
