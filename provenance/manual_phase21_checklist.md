# Phase 21 — Manual Tier-B Deploy Checklist

The automated Phase 21 Tier-A checks all passed against the built site (`_build/html`,
identical to the CI build artifact). Automated Chromium, Firefox, and WebKit widget
checks now run in CI. The remaining **Tier B** checks require the deployed URL and
must be recorded for each stable release.

After the site is live, verify these Tier-B items in a browser:

- [ ] **PER_PAGE_HTTP_200** — every page loads (200): Home, Introduction, the 7 body
  sections, Conclusion, Methods, Literature Evidence Explorer, Claim & TRUST Audit,
  and Pipeline Provenance.
- [ ] **EXTERNAL_LINK_HEALTH** — spot-check that DOI links (`https://doi.org/...`) and
  the GitHub nav link resolve.
- [ ] **Widgets render with data** — the Authorship Explorer (frontmatter) and the
  Literature Evidence Explorer populate; figure-code dropdowns expand.
- [ ] **STATUS_DISCLOSURE_VISIBLE** — not-peer-reviewed, incomplete-human-review,
  AI-assistance, and experimental-TRUST wording appears on the public site.
- [ ] **Figures display** — all 21 section figures + the Methods pipeline schematic show.
