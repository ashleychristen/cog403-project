import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
import csv

PHON_FEATURES = ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','15A','16A',
                 '17A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A','25B'
                  '26A','27A','28A','29A']


def main():
    with open('cleaned_data/modified_info_standardized.json', 'r') as f:
        data = json.load(f)
    lang_count = 0
    outfile = "coords_all.csv"
    with open(outfile, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['language', 'latitude', 'longitude'])

        language = {}
        
        lat_lst = []
        long_lst = []
        morph = []
        phon = []

        only_phon = 0
        only_morph = 0
        neither = 0
        for lang in data:
            language[lang] = {}
            language[lang]['morph_score'] = 0
            language[lang]['phon_score'] = 0


            phon_count = 0
            morph_count = 0

            phon_score = 0
            morph_score = 0
            lat = 0
            long = 0

            for feat in data[lang]:
                if feat in PHON_FEATURES:
                    phon_score += data[lang][feat]['value']
                    phon_count += 1
                elif feat in MORPH_FEATURES:
                    morph_score += data[lang][feat]['value']
                    morph_count += 1

                elif feat == "latitude":
                    lat = data[lang][feat]
                elif feat == "longitude":
                    long = data[lang][feat]
            
            if morph_count == 0 and phon_count > 0:
                print(f'morph = 0, phon = {phon_count}')
                only_phon += 1
                language[lang]['phon_score'] = phon_score / phon_count
                language[lang]['morph_score'] = morph_score
            elif morph_count > 0 and phon_count == 0:
                print(f'morph = {morph_count}, phon = {phon_count}')
                only_morph += 1
                language[lang]['phon_score'] = phon_score
                language[lang]['morph_score'] = morph_score / morph_count
            elif morph_count == 0 and phon_count == 0:
                print('both are zero')
                neither += 1
                continue
            else:
                language[lang]['phon_score'] = phon_score / phon_count
                language[lang]['morph_score'] = morph_score / morph_count
            language[lang]['latitude'] = lat
            language[lang]['longitude'] = long

            lang_count += 1
            lat_lst.append(language[lang]['latitude'])
            long_lst.append(language[lang]['longitude'])
            morph.append(language[lang]['morph_score'])
            phon.append(language[lang]['phon_score'])

            writer.writerow([lang, lat, long])
        
    full = {"lat": lat_lst, 'long': long_lst, 'morph': morph, 'phon': phon}
    
    for x in full:
        for y in full:
            if x != y:
                d1 = full[x]
                d2 = full[y]
                res = stats.pearsonr(d1, d2)

                if res[1] < 0.05:
                    # print('\n')
                    print(x, y)
                    # print(res)
    
    df = pd.DataFrame(language)
    df = df.T
    print(f'\nall languages: {lang_count}')
    print(f'morph only: {only_morph}')
    print(f'phon only: {only_phon}')
    print(f'neither: {neither}')

    corr_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f")
    plt.title(f'Correlation Matrix')
    plt.show()


main()