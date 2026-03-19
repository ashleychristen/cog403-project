"""
 first function: compute score for phonological and morphological features
                takes in list of features that were summing up
                only the languages that have features have a value 
    
    turning the data into a numerical score --> pearson correlation
    family list --> aggregate by family (average)

    between and within family

    graphs: scatter plot and regression line 
    a lot of overlapping dots --> make alpha = 0.5

 """

import json
import matplotlib.pyplot as plt
from scipy.stats.mstats import spearmanr
from scipy.stats import pearsonr
import statistics

PHON = ('2A', '3A', '4A', '6A', '7A', '8A', '11A')
MORPH = ('20A', '21A', '21B', '22A', '23A', '25B', '26A')
BOTH = ('2A', '3A', '4A', '6A', '7A', '8A', '11A', '20A', '21A', '21B', '22A', '23A', '25B', '26A')
BETWEEN = True

# load dataset
with open('modified_info.json', 'r') as f:
    data = json.load(f)

# choose languages that have a value for each of the selected features
chosen_languages = []
for language in data:

    same = 0

    feats = data[language].keys()
    for f in BOTH:
        if f in feats:
            same += 1
    
    if same == len(BOTH):

        chosen_languages.append(language)

# calculate the phonological and morphological score for each of the chosen languages (for the chosen features)
by_language = {}
families = {}

for lang in chosen_languages:
    by_language[lang] = {}
    by_language[lang]['phon_score'] = 0
    by_language[lang]['morph_score'] = 0

    morph_score = 0
    phon_score = 0
    for feat in data[lang]:
        if feat in PHON:
            phon_score += data[lang][feat]['value']
        elif feat in MORPH:
            morph_score += data[lang][feat]['value']
    
    by_language[lang]['phon_score'] = phon_score
    by_language[lang]['morph_score'] = morph_score

    # add the complexity scores just calculated to the family list
    family = data[lang]['family']
    if family not in families:
        families[family] = {}
        families[family]['phonological'] = []
        families[family]['morphological'] = []
    
    families[family]['phonological'].append(phon_score)
    families[family]['morphological'].append(morph_score)


# calculate average complexity for each language and plot

if BETWEEN:
    average_phon = []
    average_morph = []

    for fam in families:
        average_morph.append(statistics.mean(families[fam]['morphological']))
        average_phon.append(statistics.mean(families[fam]['phonological']))

    print('Pearson')
    print(pearsonr(average_morph, average_phon))
    print('Spearman')
    print(spearmanr(average_morph, average_phon))
    plt.scatter(average_morph, average_phon, alpha=0.5)
    plt.xlabel('Average Morphological Complexity')
    plt.ylabel('Average Phonological Complexity')
    plt.title('Complexity Trade Off Between Families')
    plt.show()

else:

    for fam in families:
        length = len(families[fam]['morphological'])
        if length < 2:
            print(f"{fam} only has 1 language")
        else:
            morphs = families[fam]['morphological']
            phons = families[fam]['phonological']

            print(f'\n\n{fam}')
            print(f"has {length} languages")
            print('Pearson')
            print(pearsonr(morphs, phons))
            print('Spearman')
            print(spearmanr(morphs, phons))
            plt.scatter(morphs, phons, alpha=0.5)
            plt.xlabel('Morphological Complexity')
            plt.ylabel('Phonological Complexity')
            plt.title(f"Complexity Trade Off - {fam}")
            plt.show()


        


    








