import json
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

def pearsonown(a,b):
    
    covar = np.cov(a, b, bias=True)[0][1]
    sda = np.std(a)
    sdb = np.std(b)
    corr = covar/(sda * sdb)
    
    return corr

with open('organized_info.json', 'r') as f:
    data = json.load(f)



scores = {}

phon = ('2A', '3A', '4A', '6A', '7A', '8A', '11A')
morph = ('20A', '21A', '21B', '22A', '23A', '25B', '26A')
both = ('2A', '3A', '4A', '6A', '7A', '8A', '11A', '20A', '21A', '21B', '22A', '23A', '25B', '26A')


chosen_languages = []
for language in data:

    same = 0

    feats = data[language].keys()
    for f in both:
        if f in feats:
            same += 1
    
    if same == len(both):

        chosen_languages.append(language)

print(len(chosen_languages))
for lang in chosen_languages:
    if lang not in scores:
        scores[lang] = {}
        scores[lang]['phon_score'] = 0
        scores[lang]['morph_score'] = 0
        scores[lang]['total_score'] = 0

    for feat in data[lang]:
        if feat in phon:
            scores[lang]['phon_score'] += data[lang][feat]['value']
            scores[lang]['total_score'] += data[lang][feat]['value']
        elif feat in morph:
            scores[lang]['morph_score'] += data[lang][feat]['value']
            scores[lang]['total_score'] += data[lang][feat]['value']

all_phon = []
all_morph = []
all_total = []

for lang in scores:
    all_phon.append(scores[lang]['phon_score'])
    all_morph.append(scores[lang]['morph_score'])
    all_total.append(scores[lang]['total_score'])


print(pearsonown(all_morph, all_phon))
plt.scatter(all_morph, all_phon)
plt.title(f"Morphology vs. Phonology Complexity ({len(morph)} features each)")
plt.xlabel("morphology complexity")
plt.ylabel("phonology complexity")
plt.show()



