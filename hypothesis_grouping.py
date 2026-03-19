import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr so in the end, there should be a scatterplot for the first one (dont change this graph logic), 
from collections import defaultdict

with open("organized_info.json", "r") as f:
    raw_data = json.load(f)

PHON_ORIG  = ['2A', '3A', '4A', '6A', '7A', '8A', '11A']
MORPH_ORIG = ['20A', '21A', '21B', '22A', '23A', '25B', '26A']

# ── Compute phonological and morphological scores ────────────
def compute_scores(data, phon_feats, morph_feats, require_all=True):
    phon_scores, morph_scores, families = [], [], []
    for lang_code, lang in data.items():
        if require_all and not (set(phon_feats) | set(morph_feats)).issubset(lang.keys()):
            continue

        p_sum = sum(lang[f]['value'] for f in phon_feats if f in lang and 'value' in lang[f])
        m_sum = sum(lang[f]['value'] for f in morph_feats if f in lang and 'value' in lang[f])

        if p_sum == 0 or m_sum == 0:
            continue

        phon_scores.append(p_sum)
        morph_scores.append(m_sum)
        families.append(lang.get('family', 'Unknown'))

    return phon_scores, morph_scores, families

# ── Aggregate by family ──────────────────────────────────────
def aggregate_by_family(phon_scores, morph_scores, families):
    family_dict = defaultdict(lambda: {'phon': [], 'morph': []})
    for p, m, f in zip(phon_scores, morph_scores, families):
        family_dict[f]['phon'].append(p)
        family_dict[f]['morph'].append(m)

    phon_avg, morph_avg = [], []
    family_names = []
    for f, vals in family_dict.items():
        phon_avg.append(np.mean(vals['phon']))
        morph_avg.append(np.mean(vals['morph']))
        family_names.append(f)
    return phon_avg, morph_avg, family_names

# scores (individual)
ps, ms, fams = compute_scores(raw_data, PHON_ORIG, MORPH_ORIG)

# correlations for individual languages
pearson_r, pearson_p = pearsonr(ms, ps)
spearman_r, spearman_p = spearmanr(ms, ps)

print("individual langs")
print(f"languages: {len(ps)}")
print(f"Pearson: r={pearson_r:+.4f}, p={pearson_p:.4f}")
print(f"spearman: rho={spearman_r:+.4f}, p={spearman_p:.4f}")

#aggregate scores with familiws
ps_fam, ms_fam, fam_names = aggregate_by_family(ps, ms, fams)

pearson_r_fam, pearson_p_fam = pearsonr(ms_fam, ps_fam)
spearman_r_fam, spearman_p_fam = spearmanr(ms_fam, ps_fam)

print("by family")
print(f"Families: {len(fam_names)}")
print(f"Pearson: r={pearson_r_fam:+.4f}, p={pearson_p_fam:.4f}")
print(f"Spearman: rho={spearman_r_fam:+.4f}, p={spearman_p_fam:.4f}")

# plots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# individual langs, pearson
ax = axes[0,0]
ax.scatter(ms, ps, color='blue', alpha=0.5)
coef = np.polyfit(ms, ps, 1)
xs = np.linspace(min(ms), max(ms), 100)
ax.plot(xs, np.polyval(coef, xs), color='red', linewidth=2)
ax.set_xlabel("Morphological complexity")
ax.set_ylabel("Phonological complexity")
ax.set_title("Pearson (individual langs)")

#individual langs spearman
ax = axes[0,1]
ax.scatter(ms, ps, color='green', alpha=0.5)
coef = np.polyfit(ms, ps, 1)
xs = np.linspace(min(ms), max(ms), 100)
ax.plot(xs, np.polyval(coef, xs), color='red', linewidth=2)
ax.set_title("spearman (individual langs)")
ax.set_xlabel("Morphological complexity")
ax.set_ylabel("Phonological complexity")

# families, pearson
ax = axes[1,0]
ax.scatter(ms_fam, ps_fam, color='blue', alpha=0.5)
coef = np.polyfit(ms_fam, ps_fam, 1)
xs = np.linspace(min(ms_fam), max(ms_fam), 100)
ax.plot(xs, np.polyval(coef, xs), color='red', linewidth=2)

ax.set_title("Pearon (by family)")
ax.set_xlabel("Morphological complexity")
ax.set_ylabel("Phonological complexity")

#plot 4: families, spearman
ax = axes[1,1]
ax.scatter(ms_fam, ps_fam, color='green', alpha=0.5)
coef = np.polyfit(ms_fam, ps_fam, 1)
xs = np.linspace(min(ms_fam), max(ms_fam), 100)
ax.plot(xs, np.polyval(coef, xs), color='red', linewidth=2)
ax.set_title("Spearman (by family)")
ax.set_xlabel("Morphological complexity")
ax.set_ylabel("Phonological complexity")
plt.tight_layout(pad=3.0) 
plt.show()