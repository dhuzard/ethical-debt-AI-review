import { expect, test } from '@playwright/test';

async function renderTrustWidgets(page) {
  await page.goto('/tests/browser/widget-fixture.html');
  await page.evaluate(async () => {
    const widget = (await import('/content/trust-claim-widget.mjs')).default;
    const render = (id, claimId) => widget.render({
      el: document.getElementById(id),
      model: {
        get(key) {
          return {
            claimId,
            claimText: 'The exact scored prose appears here.',
            claimType: 'empirical',
            modality: 'asserted',
            trustScore: 80,
            trustLabel: 'moderate_trust',
            evidenceRelation: 'supports',
            targetAnchor: 'claim-target',
            interactionMode: 'slideout',
            cites: '[]',
            citationContexts: '[]',
            rationale: 'null',
          }[key];
        },
      },
    });
    render('trust-one', 'claim-one');
    render('trust-two', 'claim-two');
  });
}

test('TRUST panels are single-active, keyboard operable, and expose ARIA state', async ({ page }) => {
  await renderTrustWidgets(page);
  const first = page.locator('#trust-one').locator('button.tc-card-btn');
  const second = page.locator('#trust-two').locator('button.tc-card-btn');

  await first.focus();
  await expect(page.locator('#claim-target')).toHaveClass(/tc-is-highlighted/);
  await first.press('Enter');
  await expect(first).toHaveAttribute('aria-expanded', 'true');
  await second.press('Enter');
  await expect(first).toHaveAttribute('aria-expanded', 'false');
  await expect(second).toHaveAttribute('aria-expanded', 'true');
  await page.locator('#trust-two button.tc-close').focus();
  await page.keyboard.press('Escape');
  await expect(second).toHaveAttribute('aria-expanded', 'false');
  await expect(second).toBeFocused();
});

test('Evidence Explorer renders explicit error, absent, and valid-empty states', async ({ page }) => {
  await page.goto('/tests/browser/widget-fixture.html');
  const renderState = async payload => page.evaluate(async value => {
    const widget = (await import('/content/evidence-explorer-widget.mjs')).default;
    widget.render({
      el: document.getElementById('evidence'),
      model: { get: key => key === 'evidence_data' ? value : '500px' },
    });
  }, payload);

  await renderState('{');
  await expect(page.locator('#evidence [role="alert"]')).toContainText('could not be read');
  await renderState(JSON.stringify({ load_status: 'absent', load_message: 'No package for section 10.' }));
  await expect(page.locator('#evidence [role="status"]')).toHaveText('No package for section 10.');
  await renderState(JSON.stringify({ load_status: 'loaded', sections: [{ section: 10 }], findings: [] }));
  await expect(page.locator('#evidence [role="status"]')).toContainText('0 findings');
});

test('Evidence gap view labels unavailable fields as not recorded', async ({ page }) => {
  await page.goto('/tests/browser/widget-fixture.html');
  await page.evaluate(async () => {
    const widget = (await import('/content/evidence-explorer-widget.mjs')).default;
    widget.render({
      el: document.getElementById('evidence'),
      model: { get: key => key === 'height' ? '500px' : JSON.stringify({
        load_status: 'loaded',
        sections: [{
          section: 1, title: 'Introduction', papers: 1, findings: 1, conflicts: 0,
          replication: { populated: 1, unavailable: 0 },
          evidence_gaps: { status: 'not-recorded', count: null },
          unreplicated_claims: { status: 'not-recorded', count: null },
        }],
        findings: [{ section: 1, claim: 'Finding', tier: 'replication_unknown' }],
        conflicts: [], figure_data: [],
      }) },
    });
  });
  const tab = page.getByRole('tab', { name: 'Evidence Gaps' });
  await tab.click();
  await expect(tab).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('#evidence')).toContainText('Not recorded');
  await expect(page.locator('#evidence')).toContainText('does not mean zero');
});
