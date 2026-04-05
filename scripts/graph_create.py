import matplotlib.pyplot as plt
import json
from scipy.stats import pearsonr
PHON_FEATURES = ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','16A',
                 '17A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A','25B',
                  '26A','27A','28A','29A']

feature_sets = [('2A', '13A', '23A', '25B'), ('2A', '11A', '16A', '23A', '26A', '27A'),
                ('2A', '9A', '11A', '16A', '23A', '26A', '27A', '29A'), 
                ('2A', '7A', '9A', '11A', '16A', '20A', '22A', '23A', '26A', '27A'),
                ('2A', '7A', '9A', '11A', '16A', '19A', '20A', '22A', '23A', '26A', '27A', '29A'),
                ('2A', '9A', '11A', '13A', '16A', '17A', '19A', '20A', '22A', '23A', '25B', '26A', '27A', '29A'),
                ('2A', '4A', '7A', '9A', '10A', '11A', '13A', '19A', '20A', '21B', '22A', '23A', '25B', '26A', '27A', '29A'),
                ('1A', '2A', '4A', '7A', '9A', '10A', '11A', '13A', '19A', '20A', '21B', '22A', '23A', '24A', '25B', '26A', '27A', '29A'),
                ('1A', '3A', '4A', '6A', '7A', '8A', '9A', '11A', '12A', '19A', '20A', '21A', '21B', '22A', '23A', '24A', '25B', '26A', '28A', '29A'),
                ('1A', '3A', '4A', '6A', '7A', '8A', '9A', '11A', '13A', '14A', '16A', '20A', '21A', '21B', '22A', '23A', '24A', '25B', '26A', '27A', '28A', '29A')]

def calculate_significance(phon_features, morph_features, language_data, languages):
    """
        Calculate the pearson and spearman values for a certain set of features & language list
    """
    phon_complexity = []
    morph_complexity = []

    for lang in language_data:
        if lang in languages:
            phon_score = 0
            morph_score = 0

            for feat in language_data[lang]:
                if feat in phon_features:
                    phon_score += language_data[lang][feat]['value']
                
                if feat in morph_features:
                    morph_score += language_data[lang][feat]['value']
            
            phon_complexity.append(phon_score)
            morph_complexity.append(morph_score)

    pearson = pearsonr(phon_complexity, morph_complexity)

    return pearson


def get_languages(data, feature_list):
    chosen_languages = []
    for language in data:

        same = 0

        feats = data[language].keys()
        for f in feature_list:
            if f in feats:
                same += 1
        
        if same == len(feature_list):

            chosen_languages.append(language)
    
    return chosen_languages


def main():
    filename = "cleaned_data/modified_info_standardized.json"

    with open(filename, 'r') as f:
        data = json.load(f)

    pearsons = []
    language_num = []

    feat_nums = []

    for lst in feature_sets:
        phon_features = []
        morph_features = []
        for feat in lst:
            if feat in PHON_FEATURES:
                phon_features.append(feat)
            else:
                morph_features.append(feat)

        languages = get_languages(data, lst)

        r = calculate_significance(phon_features, morph_features, data, languages)
        # print(r)
        pearsons.append(r[0])
        language_num.append(len(languages))
        feat_nums.append(len(lst))

    plt.plot(feat_nums, language_num, color='green')
    # plt.plot(feat_nums, pearsons, color="blue")
    plt.show()


main()
        
