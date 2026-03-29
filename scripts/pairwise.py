import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import combinations
from scipy.stats import binomtest, linregress
from adjustText import adjust_text
import pandas as pd

PHON_FEATURES = ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','15A','16A',
                 '17A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A', '25B',
                  '26A','27A','28A','29A']

with open('cleaned_data/modified_info_standardized.json', 'r') as f:
    data = json.load(f)

# both = ('2A', '13A', '23A', '25B')
# both = ('2A', '9A', '11A', '13A', '16A', '17A', '19A', '20A', '22A', '23A', '25B', '26A', '27A', '29A')
both = ('1A', '3A', '4A', '6A', '7A', '8A', '9A', '11A', '13A', '14A', '16A', '20A', '21A', '21B', '22A', '23A', '24A', '25B', '26A', '27A', '28A', '29A')


PHON = []
MORPH = []

for feat in both:
    if feat in PHON_FEATURES:
        PHON.append(feat)
    else:
        MORPH.append(feat)

SIMILARITY_THRESHOLD = 0.05
PHON_AND_MORPH_THRES = len(PHON)

lang_codes = list(data.keys())

pair_results = []

# find data 
for code1, code2 in combinations(lang_codes, 2):
    # make sure we only keep features that they have data for
    phon_shared  = [f for f in PHON  if f in data[code1] and f in data[code2]]
    morph_shared = [f for f in MORPH if f in data[code1] and f in data[code2]]
    
    # not enough data so we skip here
    if len(phon_shared) < PHON_AND_MORPH_THRES or len(morph_shared) < PHON_AND_MORPH_THRES:
        continue
    
    phon1 = sum(data[code1][f]['value'] for f in phon_shared)
    phon2 = sum(data[code2][f]['value'] for f in phon_shared) 
    morph1 = sum(data[code1][f]['value'] for f in morph_shared)
    morph2 = sum(data[code2][f]['value'] for f in morph_shared) 

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

# calculate scores for each language
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

# filter data for families with over 2 languages
fam_names = []
phon_scores  = []
morph_scores = []
df = {}
# df['origin'] = {'morph': 0, 'phon':0}
for fam in lang_phon:
    if len(lang_phon[fam]) >= 2:
        fam_names.append(fam)
        phon_scores.append(sum(lang_phon[fam])/len(lang_phon[fam]))
        morph_scores.append(sum(lang_morph[fam])/len(lang_morph[fam]))
        df[fam] = {'morph': sum(lang_morph[fam])/len(lang_morph[fam]), 'phon': sum(lang_phon[fam])/len(lang_phon[fam])}


df = pd.DataFrame(df)
df = df.T
# print(df)


# calculate regression & set up plot
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

print("\nRegression stats:")

print(f"r (correlation): {r:.4f}")
print(f"r squared: {r**2:.4f}")
print(f"p-value: {p_reg:.6f}")
print(f"n of families: {len(morph_scores)}")

#fig 1:plotting familiex
fig1, ax1 = plt.subplots()
plt.scatter(morph_scores, phon_scores, color='royalblue',zorder=2, alpha=0.7)

import csv
output = f"pairwise_{len(PHON)}.csv"
with open(output, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['fam_names', 'morph_scores', 'phon_scores'])

labels = []
for i in range(len(fam_names)):
    # for fam names
    # ax1.annotate(fam_names[i], (morph_scores[i], phon_scores[i]),
    #              ha='left', va='bottom',
    #              xytext=(2.5, 2),textcoords='offset points', color='black',fontsize=8 )
    labels.append(ax1.text(morph_scores[i], phon_scores[i], fam_names[i]))
    
    with open(output, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([fam_names[i], morph_scores[i], phon_scores[i]])

adjust_text(labels)
# min_val = 0
# max_val = 3.5
plt.plot([min_val, max_val], [min_val, max_val], linestyle='--', color='gray', label='Null: phon = morph')
ax1.plot(x_line, y_line, color='red', label=f'Regression (r={r:.2f}, p={p_reg:.3f})')
# slope, intercept, r, p_reg, stderr = linregress(df['morph'], df['phon'])
# plt.plot(df['morph'], intercept + slope * df['morph'], color='red')
# ax1.set_ylim(0, max_val)
# ax1.set_xlim(0, max_val)

# ax1.set_xlabel('Mean morphology score')
# ax1.set_ylabel('Mean phonology score')
# ax1.set_title('Phonology vs morphology complexity per language')
# ax1.legend( loc='upper right')

# fig1.subplots_adjust(right=0.72)



plt.show()