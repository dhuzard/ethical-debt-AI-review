# Deploying the live site

The review builds to a self-contained static site with `myst build --html` (output:
`_build/html`, ~41 MB). GitHub Pages is unavailable for this private repository on the
current plan, so host the built site on any static host. The built HTML uses
**root-absolute** asset paths (e.g. `/myst-theme.css`), so it must be served at a
**domain root** (Netlify, Cloudflare Pages, and most static hosts do this) — not under a
sub-path like `example.com/repo/`.

Figures are committed as PNGs; the notebooks in `figures/notebooks/` are reproducibility
artifacts only. The build never re-executes them, so no Python is needed to deploy.

## Option A — Netlify (repo connect, recommended)
A `netlify.toml` is committed (build = `npm install -g mystmd && npm install yaml &&
myst build --html`, publish = `_build/html`).
1. netlify.com → Add new site → Import from Git → pick this repo.
2. Netlify reads `netlify.toml` automatically. Deploy.

**Or without connecting the repo** (deploy the already-built folder):
```bash
myst build --html
npx netlify-cli deploy --prod --dir=_build/html
```
**Or** drag-and-drop the `_build/html` folder onto app.netlify.com/drop.

## Option B — Cloudflare Pages
Dashboard → Workers & Pages → Create → Pages → Connect to Git → this repo, then set:
- Build command: `npm install -g mystmd && npm install yaml && myst build --html`
- Build output directory: `_build/html`
- (No framework preset; Node 18.)

**Or** deploy the built folder directly:
```bash
myst build --html
npx wrangler pages deploy _build/html
```

## Option C — any static host / internal server
```bash
myst build --html
# then serve/copy the _build/html directory at the web root, e.g.:
#   rsync -a _build/html/ user@server:/var/www/ethical-debt/
```

## After deploy — verify (Tier-B checklist)
See `provenance/manual_phase21_checklist.md`: every page returns 200; DOI/nav links
resolve; the Authorship Explorer and Evidence Database widgets populate; figure
"📓 Figure code" dropdowns expand; all 21 figures + the Methods schematic display.
