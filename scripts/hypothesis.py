import json
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
from scipy.stats.mstats import spearmanr
from scipy.stats import pearsonr
import statsmodels.api as sm 
import pandas as pd


PHON_FEATURES = ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','15A','16A',
                 '17A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A', '25B',
                  '26A','27A','28A','29A']

with open('cleaned_data/modified_info_standardized.json', 'r') as f:
    data = json.load(f)



scores = {}

both = ('2A', '13A', '23A', '25B')





phon = []
morph = []

for feat in both:
    if feat in PHON_FEATURES:
        phon.append(feat)
    else:
        morph.append(feat)

# determine which languages have values for the selected features
chosen_languages = []
for language in data:

    same = 0

    feats = data[language].keys()
    for f in both:
        if f in feats:
            same += 1
    
    if same == len(both):

        chosen_languages.append(language)

# determine scores for languages that have all of the selected features
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
        elif feat == "latitude":
            scores[lang]['latitude'] = data[lang][feat]
        elif feat == "longitude":
            scores[lang]['longitude'] = data[lang][feat]


# create dataframe from information to prepare for multiple linear regression

df = pd.DataFrame(scores)
df = df.T
# print(df)

all_phon = df['phon_score']
all_morph = df['morph_score']
long = df['latitude']
lat = df['longitude']


independent_var = df[['morph_score', 'latitude', 'longitude']]
dependent_var = all_phon

X = sm.add_constant(independent_var)
model = sm.OLS(dependent_var, X)
results = model.fit()
print(results.summary())


print(f'feature list: {both}')
print(f'number of languages: {len(chosen_languages)}')

# calculate statistical analyses 

print('pearson')
pearson = pearsonr(all_morph, all_phon)
print(pearson)
print('spearman')
spearman = spearmanr(all_morph, all_phon)
print(spearman)

slope, intercept, r, p, se = linregress(df['morph_score'], df['phon_score'])
print(f'slope: {slope}')

# print('multiple linear regression')
plt.scatter(all_morph, all_phon, alpha=0.5)
plt.plot(df['morph_score'], intercept + slope * df['morph_score'], color='#097969')

# plot diagnonal null hypothesis line
# mn = 0
# mx = len(phon)
# plt.plot([mn, mx], [mn, mx], linestyle='--', color='gray')


plt.title(f"Morphology vs. Phonology Complexity ({len(both) / 2} features each)")
plt.xlabel("Morphology Complexity")
plt.ylabel("Phonology Complexity")
plt.savefig(f"graphs/optimized_correlation/scatter_plot_{len(both)/2}.png")
plt.show()


