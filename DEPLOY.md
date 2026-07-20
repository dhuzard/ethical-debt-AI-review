# Reproduce, release, and deploy

The public site is a preview built from `main`. Release candidates are immutable
integration references: they are **not peer reviewed**, **not fully
human-adjudicated**, and use an **experimental TRUST** audit signal.

## Pinned environment

- Node.js 24
- Python 3.11
- npm dependencies from `package-lock.json` (`npm ci`)
- Python dependencies from exact pins in `requirements.txt`

```bash
npm ci --no-audit --no-fund
python -m pip install --requirement requirements.txt
npx playwright install chromium firefox webkit
```

## Complete local reproduction

```bash
npm run validate
npm test
npm run test:browser
python scripts/check_deterministic_figures.py
npm run build:deterministic
```

The figure check executes every notebook twice without modifying the committed
notebooks, compares both PNG sets byte-for-byte, and verifies the frozen release
hashes. The deterministic build command runs MyST twice and compares every output
file after normalizing only MyST's presentation-only random AST keys and derived
image DOM IDs. The final site remains in `_build/html`.

To reproduce only the canonical interoperability export:

```bash
node scripts/export-oratlas.js
node scripts/validate-oratlas.js
node scripts/build-oratlas-fixtures.js
```

## Release-candidate procedure

1. Confirm `git status --short` is empty at the intended commit.
2. Run `npm run release:check`.
3. Review the limitations in `RELEASE_CONTRACT.md` and release notes.
4. Create an annotated tag, for example `git tag -a v0.1.0-rc.1 -m "Reference prerelease rc.1"`.
5. Run `node scripts/validate-release.js --tag v0.1.0-rc.1`.
6. Push the tag and publish a GitHub **prerelease** whose notes repeat the public
   status and limitations. ORAtlas must ingest this tag/commit, not a branch.

Tags are immutable. Corrections use a new release candidate. Stable `v1.0.0`
requires completion of the human scientific-review queue and the manual live-site
checks; a release candidate does not.

## DOI/Zenodo

`.zenodo.json` is ready for a review-specific deposit. Do not reuse the template
DOI and do not mint the review DOI before a stable archived release exists. After
deposit, add the issued DOI to `.zenodo.json`, `README.md`, `FAIR.md`, and the
release record in one versioned change.

## Deployment

GitHub Actions validates pull requests and deploys GitHub Pages only from `main`.
The workflow sets `BASE_URL=/ethical-debt-AI-review`. After deployment, complete
`provenance/manual_phase21_checklist.md`, including page responses, DOI links,
authorship, both evidence layers, figure displays, and TRUST interactions.
