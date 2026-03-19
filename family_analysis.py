import json
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.stats import binomtest

with open('modified_info_standardized.json', 'r') as f:
    data = json.load(f)

PHON  = ('1A', '2A', '3A', '4A', '6A', '7A', '8A', '9A', '10A', '11A',
         '12A', '13A', '14A', '15A', '16A', '17A', '19A')
MORPH = ('20A', '21A', '21B', '22A', '23A', '24A', '25B', '26A', '27A', '28A', '29A')

SIMILARITY_THRESHOLD = 0.05
PHON_AND_MORPH_THRES = 6  #minimum shared features

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
within_diffs = []
across_diffs = []
for code1, code2 in combinations(lang_codes, 2):
    phon_n, _  = score_pair(data[code1], data[code2], PHON)
    morph_n, _ = score_pair(data[code1], data[code2], MORPH)
    if phon_n < PHON_AND_MORPH_THRES or morph_n < PHON_AND_MORPH_THRES:
        continue

    phon_shared  = [f for f in PHON if f in data[code1] and f in data[code2]]
    morph_shared = [f for f in MORPH if f in data[code1] and f in data[code2]]

    phon1  = sum(data[code1][f]['value'] for f in phon_shared) / len(phon_shared)
    phon2  = sum(data[code2][f]['value'] for f in phon_shared) / len(phon_shared)
    morph1 = sum(data[code1][f]['value'] for f in morph_shared) / len(morph_shared)
    morph2 = sum(data[code2][f]['value'] for f in morph_shared) / len(morph_shared)

    diff1 = phon1 - morph1
    diff2 = phon2 - morph2

    same_family = data[code1].get('family', '') == data[code2].get('family', '')

    if same_family:
        within_diffs.extend([diff1, diff2])
    else:
        across_diffs.extend([diff1, diff2])

print(f"within-family languages: {len(within_diffs)}")
print(f"across-family languages: {len(across_diffs)}")
print(f"within mean diff: {np.mean(within_diffs):.3f}")
print(f"across mean diff: {np.mean(across_diffs):.3f}")

export = {"within_family": within_diffs, "across_family": across_diffs}
with open('family_diffs.json', 'w') as f:
    json.dump(export, f)

#within-fam
fig1, ax1 = plt.subplots(figsize=(7,5))
ax1.hist(within_diffs, bins=30, color='green', edgecolor='white')
ax1.axvline(0, color='gray', linestyle='--', label='no difference')
ax1.axvline(np.mean(within_diffs), color='red', label=f'mean = {np.mean(within_diffs):.3f}')
ax1.set_xlabel('Phonology− morphology complexity')
ax1.set_ylabel('Count')
ax1.set_title('Within-family phonology−morphology complexity')
ax1.legend(fontsize=8)
plt.tight_layout()


# across-fam
fig2, ax2 = plt.subplots(figsize=(7,5))
ax2.hist(across_diffs, bins=30, color='blue', edgecolor='white')
ax2.axvline(0, color='gray', linestyle='--', label='no difference')
ax2.axvline(np.mean(across_diffs), color='red', label=f'mean = {np.mean(across_diffs):.3f}')
ax2.set_xlabel('Phonology−morphology complexity')
ax2.set_ylabel('count')
ax2.set_title('Across-family phonology−morphology complexity')
ax2.legend(fontsize=8)
plt.tight_layout()
plt.show()