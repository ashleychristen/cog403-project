import json
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.stats import pearsonr, binomtest

with open('cleaned_data/modified_info_standardized.json', 'r') as f:
    data = json.load(f)

PHON  = ('2A', '9A', '11A', '13A', '16A', '17A', '19A')
MORPH = ('20A', '22A', '23A', '25B', '26A', '27A', '29A')

PHON_AND_MORPH_THRES = 2  #minimum shared features

lang_codes = list(data.keys())

within_corrs = []
across_corrs = []

for code1, code2 in combinations(lang_codes, 2):
    # make sure we only keep features that they have data for
    phon_shared  = [f for f in PHON  if f in data[code1] and f in data[code2]]
    morph_shared = [f for f in MORPH if f in data[code1] and f in data[code2]]

    #not enough data so we skip here
    if len(phon_shared) < PHON_AND_MORPH_THRES or len(morph_shared) < PHON_AND_MORPH_THRES:
        continue

    morph1_vals = [data[code1][f]['value'] for f in morph_shared]
    morph2_vals = [data[code2][f]['value'] for f in morph_shared]
    phon1_vals  = [data[code1][f]['value'] for f in phon_shared]
    phon2_vals  = [data[code2][f]['value'] for f in phon_shared]
    #get our complexity scores
    morph_vec = morph1_vals + morph2_vals
    phon_vec  = phon1_vals  + phon2_vals

    #undefined correlation
    if np.std(morph_vec) == 0 or np.std(phon_vec) == 0:
        continue

    r, p_value = pearsonr(morph_vec, phon_vec)

    same_family = data[code1]['family'] == data[code2]['family']
    if same_family:
        within_corrs.append(r)
    else:
        across_corrs.append(r)

def analyze(corrs, label):
    pos = sum(1 for r in corrs if r > 0)
    pval = binomtest(pos, len(corrs), p=0.5, alternative='less')
    print(f"\n{label}")
    print(f"number of pairs: {len(corrs)}")
    print(f" mean r: {np.mean(corrs):.3f}")
    print(f"binomtest p-val: {pval.pvalue:.4f}")
    return pval.pvalue

#get stats
w_p = analyze(within_corrs, "Within-family")
a_p = analyze(across_corrs, "Across-family")

def plot_violin_box(ax, corrs, colour, label, binom_p):
    parts = ax.violinplot(corrs, positions=[1], showmedians=False,
                          showextrema=False, bw_method=0.3)
    for pc in parts['bodies']:
        pc.set_facecolor(colour)
        pc.set_alpha(0.5)
        pc.set_zorder(1)

    #boxplot inside the violin
    
    bp = ax.boxplot(corrs, positions=[1], widths=0.06,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=2.5, zorder=5),
                    boxprops=dict(facecolor= colour, color='black', zorder=4),
                    whiskerprops=dict(color='black', zorder=4),
                    capprops=dict(color='black', zorder=4))

    ax.axhline(0, color='gray', linestyle='--', linewidth=1, label='r = 0', zorder=2)
    ax.axhline(np.mean(corrs), color="orchid", linestyle='-',
               linewidth=1.5, alpha=0.9,
               label=f'mean r = {np.mean(corrs):.3f}', zorder=3)
    ax.set_ylim(-1.15, 1.15)
    ax.set_yticks(np.arange(-1.0, 1.1, 0.25))

    ax.set_xticks([1])
    ax.set_xticklabels([label], fontsize=11)

    ax.set_ylabel('Pearson r  (morph vs phon)', fontsize=10)
    ax.set_title(
        f'{label} pairwise correlations\n'
        f'n={len(corrs)},  mean r={np.mean(corrs):.3f}',
        fontsize=11
    )
    ax.legend(fontsize=8, loc='upper right')



# fig1, ax1 = plt.subplots(figsize=(5, 7))
# plot_violin_box(ax1, within_corrs, 'palegreen', 'Within-family', w_p)

# plt.tight_layout()

# fig2, ax2 = plt.subplots(figsize=(5, 7))
# plot_violin_box(ax2, across_corrs, 'royalblue', 'Across-family', a_p)
# plt.tight_layout()

plt.violinplot([within_corrs, across_corrs])
plt.boxplot([within_corrs, across_corrs])
plt.show()