"""fig_sec5_vcg_reduction — Reduction dividend of virtual control groups.

Two panels (never one axis, per the figure comparability decision):
  (a) three preclinical VCG proposals converging on ~25% control-animal
      reduction (non-independent estimates, annotated);
  (b) a human device-trial Bayesian-borrowing enrolment reduction
      (~37%, both arms) — different species/unit/scope, plotted separately.

Data are read from the section evidence file; study labels come from the
section author-name table; colours from shared_style (Okabe-Ito).
"""
import os
import json
import numpy as np
import matplotlib.pyplot as plt


def _repo_path(rel):
    for base in ['.', '..', '../..', '../../..', os.path.dirname(os.path.abspath(__file__)) + '/../..']:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return os.path.normpath(p)
    raise FileNotFoundError(rel)


# style module lives alongside the notebooks
import sys
sys.path.insert(0, os.path.dirname(_repo_path('figures/notebooks/shared_style.py')))
from shared_style import COLORS, apply_style, save_figure  # noqa: E402

apply_style()

EV = json.load(open(_repo_path('evidence/evidence_section_05.json'), encoding='utf-8'))
AT = json.load(open(_repo_path('evidence/authortable_section_05.json'), encoding='utf-8'))
CM = json.load(open(_repo_path('evidence/citemap_section_05.json'), encoding='utf-8'))


def label_for(doi):
    a = AT[CM[doi]]
    return "%s\n%s" % (a['citet_display'], a['year'])


fd = next(x for x in EV['figure_data']
          if x['comparison_id'] == 'vcg-hcd-animal-reduction-estimates')
papers = fd['papers']

# Panel A: preclinical percentage reductions (value like "25%")
pre = [p for p in papers if str(p['value']).strip().endswith('%')]
# Panel B: clinical device-trial enrolment (value like "1,497 vs 2,386")
dev = next(p for p in papers if 'vs' in str(p['value']))

pre_labels = [label_for(p['doi']) for p in pre]
pre_vals = [float(str(p['value']).replace('%', '')) for p in pre]
pre_abstract = [p['text_access'] != 'fulltext' for p in pre]

dev_after, dev_before = [int(s.replace(',', '').strip())
                         for s in str(dev['value']).split('vs')]
dev_reduction = 100.0 * (dev_before - dev_after) / dev_before

fig, (axA, axB) = plt.subplots(1, 2, figsize=(14, 6.2),
                               gridspec_kw={'width_ratios': [3, 2]})

# ── Panel A: preclinical control-animal reduction ──
xA = np.arange(len(pre))
barsA = axA.bar(xA, pre_vals, width=0.62, color=COLORS['repayment'],
                edgecolor=COLORS['ink'], linewidth=0.5, hatch='//', zorder=3)
for i, (b, v, ab) in enumerate(zip(barsA, pre_vals, pre_abstract)):
    txt = ("%d%%" % v) + ('*' if ab else '')
    axA.text(b.get_x() + b.get_width() / 2, v + 0.6, txt,
             ha='center', va='bottom', fontsize=12, fontweight='bold',
             color=COLORS['ink'])
axA.axhline(25, color=COLORS['neutral_baseline'], lw=0.75, ls='--', zorder=1)
axA.set_xticks(xA)
axA.set_xticklabels(pre_labels, fontsize=10.5)
axA.set_ylim(0, 33)
axA.set_ylabel('Control-animal reduction (%)')
axA.set_title('(a) Preclinical: virtual control groups', fontsize=13, loc='left')
axA.annotate('Not independent: the later two cite the\noriginal 25% concept, not re-derive it',
             xy=(1.0, 25), xytext=(0.15, 31),
             fontsize=9.5, color=COLORS['ink'],
             ha='left', va='center')

# ── Panel B: clinical enrolment reduction (before/after) ──
xB = np.array([0, 1])
valsB = [dev_before, dev_after]
colB = [COLORS['neutral_baseline'], COLORS['secondary_cat']]
barsB = axB.bar(xB, valsB, width=0.6, color=colB,
                edgecolor=COLORS['ink'], linewidth=0.5, zorder=3)
for b, v in zip(barsB, valsB):
    axB.text(b.get_x() + b.get_width() / 2, v + 40, "{:,}".format(v),
             ha='center', va='bottom', fontsize=12, fontweight='bold',
             color=COLORS['ink'])
axB.set_xticks(xB)
axB.set_xticklabels(['Frequentist\n(no borrowing)', 'Bayesian borrowing\n(congruent)'],
                    fontsize=10.5)
axB.set_ylim(0, dev_before * 1.22)
axB.set_ylabel('Enrolled patients (both arms)')
axB.set_title('(b) Clinical: %s' % label_for(dev['doi']).replace('\n', ' '),
              fontsize=13, loc='left')
# reduction bracket
ytop = dev_before * 1.10
axB.annotate('', xy=(1, dev_after + 40), xytext=(1, ytop),
             arrowprops=dict(arrowstyle='-', color=COLORS['ink'], lw=0.8))
axB.annotate('', xy=(0, dev_before + 40), xytext=(0, ytop),
             arrowprops=dict(arrowstyle='-', color=COLORS['ink'], lw=0.8))
axB.annotate('', xy=(0, ytop), xytext=(1, ytop),
             arrowprops=dict(arrowstyle='<->', color=COLORS['debt'], lw=1.4))
axB.text(0.5, ytop + 30, '~%d%% fewer' % round(dev_reduction),
         ha='center', va='bottom', fontsize=11.5, fontweight='bold',
         color=COLORS['debt'])

fig.text(0.01, -0.02,
         "* value from abstract; full text not accessible. "
         "Panels use different units (animals vs trial participants) and separate axes — not a common scale.",
         fontsize=9, color=COLORS['gray_500'], ha='left', style='italic')

fig.tight_layout()
out = _repo_path('figures') + '/fig_sec5_vcg_reduction.png'
save_figure(fig, out)
print('saved:', out)
