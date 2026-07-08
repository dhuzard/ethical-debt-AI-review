# Phase 21 — Manual Tier-B Deploy Checklist

The automated Phase 21 Tier-A checks all passed against the built site (`_build/html`,
identical to the CI build artifact). The two **Tier B** checks require a live deployed
URL, which is currently **blocked**: GitHub Pages cannot be enabled for
`dhuzard/ethical-debt-AI-review` because it is a private repository on a plan that does
not include Pages for private repos (`POST /pages` → HTTP 422). The CI **build** step
succeeds; only the **deploy-pages** step fails.

## To publish the live site, choose one:

1. **Make the repository public** (Settings → General → Change visibility → Public).
   GitHub Pages is free for public repos; the existing `.github/workflows/deploy.yml`
   will then deploy on the next push to `main`. This is the simplest option.
2. **Upgrade the GitHub plan** (Pro/Team/Enterprise) to enable Pages on a private repo.
3. **Deploy the built artifact elsewhere** — the `_build/html` directory (or the CI
   `github-pages` artifact) is a self-contained static site that can be hosted on
   Netlify, Cloudflare Pages, an internal server, etc.

After the site is live, verify these Tier-B items in a browser:

- [ ] **PER_PAGE_HTTP_200** — every page loads (200): Home, Introduction, the 7 body
  sections, Conclusion, Methods, Evidence Database, Pipeline Provenance.
- [ ] **EXTERNAL_LINK_HEALTH** — spot-check that DOI links (`https://doi.org/...`) and
  the GitHub nav link resolve.
- [ ] **Widgets render with data** — the Authorship Explorer (frontmatter) and the
  Evidence Database explorer populate; figure "📓 Figure code" dropdowns expand.
- [ ] **Figures display** — all 21 section figures + the Methods pipeline schematic show.
