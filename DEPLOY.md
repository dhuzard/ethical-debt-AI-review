# Deploying the live review

The public preview is built and deployed by `.github/workflows/deploy.yml` from the
`trust-scores` branch. After the TRUST migration is merged, `main` becomes the canonical
deployment source. Both branches run the same validation, notebook-execution, and MyST build
steps before GitHub Pages deployment.

Expected public URL:

<https://dhuzard.github.io/ethical-debt-AI-review/>

## Local build

```bash
npm ci
node scripts/validate-trust.js
node scripts/test-trust-validator.js
node --test tests/*.test.mjs
myst build --html
```

The generated site is written to `_build/html`. The workflow sets
`BASE_URL=/ethical-debt-AI-review` so assets resolve under the GitHub Pages project path.

## Release policy

- Preview releases are tagged from `trust-scores` and clearly disclose the incomplete human
  adjudication pass.
- Stable releases are tagged from `main` only after the required human review is complete.
- Oratlas demonstrations should select an exact release or tag, never the moving branch.
- A review-specific DOI should be added only after a matching archived release exists.

## Post-deployment checks

Use `provenance/manual_phase21_checklist.md` to verify page responses, internal and DOI links,
the Authorship Explorer, Evidence Database, TRUST claim cards, figure-code dropdowns, and all
figures.
