import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json

PHON_FEATURES = ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','15A','16A',
                 '17A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A','25B'
                  '26A','27A','28A','29A']


def main():
    with open('modified_info_standardized.json', 'r') as f:
        data = json.load(f)

    language = {}
    

    for lang in data:
        language[lang] = {}
        language[lang]['morph_score'] = 0
        language[lang]['phon_score'] = 0

        for feat in data[lang]:
            if feat in PHON_FEATURES:
                language[lang]['phon_score'] += data[lang][feat]['value']
            elif feat in MORPH_FEATURES:
                language[lang]['morph_score'] += data[lang][feat]['value']

            elif feat == "latitude":
                language[lang]['latitude'] = data[lang][feat]
            elif feat == "longitude":
                language[lang]['longitude'] = data[lang][feat]
    
    
    df = pd.DataFrame(language)
    df = df.T

    corr_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title(f'Correlation Matrix')
    plt.show()


main()