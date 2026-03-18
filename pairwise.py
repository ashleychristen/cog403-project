import json
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from itertools import combinations
from scipy.stats import binomtest

with open('modified_info_standardized.json', 'r') as f:
    data = json.load(f)

PHON  = ('1A', '2A', '3A', '4A', '6A', '7A', '8A', '9A', '10A', '11A', '12A', '13A', '14A', '15A', '16A', '17A', '19A')
MORPH = ('20A', '21A', '21B', '22A', '23A', '24A', '25B', '26A', '27A', '28A', '29A')
ALL   = PHON + MORPH

SIMILARITY_THRESHOLD = 0.1

def score_pair(lang1, lang2, features):
    n = 0
    k = 0
    for feat in features:
        if feat in lang1 and feat in lang2:
            n += 1
            if abs(lang1[feat]['value'] - lang2[feat]['value']) <= SIMILARITY_THRESHOLD:
                k += 1
    return n, k

lang_codes = list(data.keys())

pair_results = []
for code1, code2 in combinations(lang_codes, 2):
    n, k = score_pair(data[code1], data[code2], ALL)
    if n >= 5:
        pair_results.append((code1, code2, n, k))

# sort by largest similariteis descending
pair_results.sort(
    key=lambda x: (x[3] / x[2], x[2]),
    reverse=True
)
TOP_N = 25
bar_labels = []
bar_n      = []
bar_pvals  = []

for i in range(TOP_N):
    code1 = pair_results[i][0]
    code2 = pair_results[i][1]
    n     = pair_results[i][2]
    k     = pair_results[i][3]
    pval  = binomtest(k, n, p=0.5, alternative='greater').pvalue
    name1 = data[code1].get('language_name', code1)[:16]
    name2 = data[code2].get('language_name', code2)[:16]
    bar_labels.append(f"{name1} / {name2}")
    bar_n.append(n)
    bar_pvals.append(pval)
    
# per-language phon vs morph scores
lang_phon  = {}
lang_morph = {}
for code in lang_codes:
    lang = data[code]
    phon_vals  = [lang[f]['value'] for f in PHON if f in lang]
    morph_vals = [lang[f]['value'] for f in MORPH if f in lang]
    if len(phon_vals) >= 3 and len(morph_vals) >= 3:
        lang_phon[code]  = sum(phon_vals)  / len(phon_vals)
        lang_morph[code] = sum(morph_vals) / len(morph_vals)

plot_codes   = list(lang_phon.keys())
phon_scores  = [lang_phon[c]  for c in plot_codes]
morph_scores = [lang_morph[c] for c in plot_codes]
families     = [data[c].get('family', 'Unknown') for c in plot_codes]

# get unique families and number
unique_families = sorted(set(families))
num_families = len(unique_families)
print(f"Number of unique families: {num_families}")

# assign each family a unique color from a colormap
cmap = plt.get_cmap('tab20', num_families)  # generate num_families colors
family_color = {f: cmap(i) for i, f in enumerate(unique_families)}

# map each language to its family color
colors = [family_color[f] for f in families]

# plot
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
ax1 = axes[0]
ax2 = axes[1]

# scatterplot of phon vs morph
ax1.scatter(phon_scores, morph_scores, c=colors, s=20, alpha=0.6)

# diagonal line
mn = min(phon_scores + morph_scores)
mx = max(phon_scores + morph_scores)
ax1.plot([mn, mx], [mn, mx], linestyle='--', color='gray')

ax1.set_xlabel('mean phon score')
ax1.set_ylabel('mean morph score')
ax1.set_title('phon vs morph')

# legend (only families with >2 languages)
family_count = {f: families.count(f) for f in unique_families}
handles = [mpatches.Patch(color=family_color[f], label=f)
           for f in unique_families if family_count[f] > 2]

#ax1.legend(handles=handles, title='family', fontsize=8, title_fontsize=9, framealpha=0.9, ncol=2)
#subplot 2: horizontal bar chart, bar length = n, color = p-value


y_pos = range(TOP_N)
colors = ['red' if p < 0.05 else "blue" for p in bar_pvals]

ax2.barh(y_pos, bar_n, color=colors)

#labels for bars
for i in range(TOP_N):
    ax2.text(bar_n[i] + 0.1, i,
             f'n={bar_n[i]}, p={bar_pvals[i]:.3f}',
             va='center', fontsize=7)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(bar_labels, fontsize=7)
ax2.invert_yaxis()

ax2.set_xlabel('number of matching features')
ax2.set_title(f'top {TOP_N} most similar pairs')

ax2.set_xlim(0, max(bar_n) + 2)

plt.tight_layout()
plt.show()
