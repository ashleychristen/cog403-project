import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json

SECTIONS = {
    'phonological': ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','15A','16A',
                 '17A','19A'],

    'morphological': ['20A','21A','21B','22A','23A','24A', '25B',
                  '26A','27A','28A','29A']
}

SECT = 'phonological'

def main():
    with open('modified_info_standardized.json', 'r') as f:
        data = json.load(f)

    chosen_languages = []
    for language in data:

        same = 0

        feats = data[language].keys()
        for f in SECTIONS[SECT]:
            if f in feats:
                same += 1
        
        if same == len(SECTIONS[SECT]):

            chosen_languages.append(language)


    language = {}

    for lang in data:
        if lang in chosen_languages:
            language[lang] = {}
            for feat in data[lang]:
                if feat in SECTIONS[SECT]:
                    language[lang][feat] = data[lang][feat]['value']
    
    
    df = pd.DataFrame(language)
    df = df.T

    print(f'num of languages: {len(chosen_languages)}')
    corr_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title(f'Correlation Matrix - {SECT} features')
    plt.show()


main()