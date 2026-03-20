import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import combinations
from scipy.stats import binomtest, linregress

with open('cleaned_data/modified_info_standardized.json', 'r') as f:
    data = json.load(f)

PHON  = ('2A', '9A', '11A', '13A', '15A', '16A', '17A')
MORPH = ( '20A', '22A', '23A', '25B', '26A', '27A', '29A')
SIMILARITY_THRESHOLD = 0.05
PHON_AND_MORPH_THRES = 7

lang_codes = list(data.keys())

def score_pair(lang1, lang2, features):
    shared_count = 0
    similar_count = 0
    for feat in features:
        if feat in lang1 and feat in lang2:
            shared_count += 1
            diff = abs(lang1[feat]['value'] - lang2[feat]['value'])
            if diff <= SIMILARITY_THRESHOLD:
                similar_count += 1
    return shared_count, similar_count 
pair_results = []

for code1, code2 in combinations(lang_codes, 2):
    # make sure we only keep features that they have data for
    phon_shared  = [f for f in PHON  if f in data[code1] and f in data[code2]]
    morph_shared = [f for f in MORPH if f in data[code1] and f in data[code2]]

    #not enough data so we skip here
    if len(phon_shared) < PHON_AND_MORPH_THRES or len(morph_shared) < PHON_AND_MORPH_THRES:
        continue

    phon1 = sum(data[code1][f]['value'] for f in phon_shared) / len(phon_shared)
    phon2 = sum(data[code2][f]['value'] for f in phon_shared) / len(phon_shared)
    morph1 = sum(data[code1][f]['value'] for f in morph_shared) / len(morph_shared)
    morph2 = sum(data[code2][f]['value'] for f in morph_shared) / len(morph_shared)

    supports = False
    if (phon1 > morph1 and morph2 > phon2) or (morph1 > phon1 and phon2 > morph2):
        supports = True

    same_family = False
    if data[code1].get('family', '') == data[code2].get('family', ''):
        same_family = True

    pair_results.append((code1, code2, phon1, morph1, phon2, morph2, supports, same_family))

total_pairs = len(pair_results)
supporting_count = 0
for p in pair_results:
    if p[6]:
        supporting_count += 1

pval = binomtest(supporting_count, total_pairs, p=0.5, alternative='greater').pvalue

print("total pairs:", total_pairs)
print("supporting:", supporting_count, "/", total_pairs, "({:.3f})".format(supporting_count/total_pairs))
print("p-value:", pval)
print("threshold:", PHON_AND_MORPH_THRES)

lang_phon = {}
lang_morph = {}

for code in lang_codes:
    lang = data[code]
    phon_vals =[lang[f]['value'] for f in PHON  if f in lang]
    morph_vals = [lang[f]['value'] for f in MORPH if f in lang]

    if len(phon_vals) < PHON_AND_MORPH_THRES or len(morph_vals) < PHON_AND_MORPH_THRES:
        continue

    family = lang.get('family', 'Unknown')
    phon_score  = sum(phon_vals) #complexity score for phonology
    morph_score = sum(morph_vals)

    if family not in lang_phon:
        lang_phon[family]  = []
        lang_morph[family] = []

    lang_phon[family].append(phon_score)
    lang_morph[family].append(morph_score)
fam_names = []
phon_scores  = []
morph_scores = []

for fam in lang_phon:
    if len(lang_phon[fam]) >= 2:
        fam_names.append(fam)
        phon_scores.append(sum(lang_phon[fam])/len(lang_phon[fam]))
        morph_scores.append(sum(lang_morph[fam])/len(lang_morph[fam]))

slope, intercept, r, p_reg, stderr = linregress(morph_scores, phon_scores)
x_line = []
y_line = []
min_val = min(morph_scores + phon_scores)
max_val = max(morph_scores + phon_scores)
step = (max_val - min_val) / 200
for i in range(201):
    x = min_val + i * step
    x_line.append(x)
    y_line.append(slope * x + intercept)

#fig 1:plotting familiex
fig1, ax1 = plt.subplots()
ax1.scatter(morph_scores, phon_scores, color='blue',zorder=2)

for i in range(len(fam_names)):
    # for fam names
    ax1.annotate(fam_names[i], (morph_scores[i], phon_scores[i]),
                 ha='left', va='bottom',
                 xytext=(3, 2),textcoords='offset points', color='black',fontsize=4 )

ax1.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='gray', label='Null: phon = morph')
ax1.plot(x_line, y_line, color='red', label=f'Regression (r={r:.2f}, p={p_reg:.3f})')

ax1.set_xlabel('Mean morphology score')
ax1.set_ylabel('Mean phonology score')
ax1.set_title('Phonology vs morphology complexity per language')
ax1.legend( loc='upper right')

fig1.subplots_adjust(right=0.72)



# # fig 2, all pairs
# fig2, ax2 = plt.subplots(figsize=(8, 7))
# ax2.set_facecolor('white')

# colours_support = ["red" if p[6] else "gray" for p in pair_results]
# x_vals = [p[3] for p in pair_results]
# y_vals = [p[2] for p in pair_results]
# ax2.scatter(x_vals, y_vals, c=colours_support, s=8, alpha=0.4)

# mn2 = min(x_vals + y_vals)
# mx2 = max(x_vals + y_vals)
# ax2.plot([mn2, mx2], [mn2, mx2], linestyle='--', color='gray')

# slope2, intercept2, r2, p_reg2, stderr = linregress(x_vals, y_vals)
# x_line2 = [mn2, mx2]
# y_line2 = [slope2 * mn2 + intercept2, slope2 * mx2 + intercept2]
# ax2.plot(x_line2, y_line2, color='blue')
# ax2.set_xlabel('Morphology score (1st language)')
# ax2.set_ylabel('Phonology score (1st language)')
# ax2.set_title(f'All pairs for language 1\nRed = supports tradeoff ({supporting_count}/{total_pairs})')
 
# handles2 = [
#     mpatches.Patch(color='red'),
#     mpatches.Patch(color='gray'),
#     plt.Line2D([0], [0], linestyle='--', color='gray'),
#     plt.Line2D([0], [0], color='blue')
# ]
# labels2 = [
#     f'Supports ({supporting_count}/{total_pairs})',
#     'Does not support hypothesis',
#     'Null: phon = morph',
#     f'Regression (r={r2:.2f}, p={p_reg2:.3f})'
# ]
# ax2.legend(handles=handles2, labels=labels2,
#            bbox_to_anchor=(1.01, 1), loc='upper left',
#            borderaxespad=0, fontsize=7)
 
# fig2.subplots_adjust(right=0.72)

plt.show()