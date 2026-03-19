import json
from scipy.stats.mstats import spearmanr
from scipy.stats import pearsonr
import itertools

PHON_FEATURES = ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','15A','16A',
                 '17A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A','25B',
                  '26A','27A','28A','29A']

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
    spearman = spearmanr(phon_complexity, morph_complexity)

    return pearson, spearman


def main():
    filename = "modified_info_standardized.json"

    with open(filename, 'r') as f:
        data = json.load(f)

    
    filename = "modified_feature_list.json"
    with open(filename, 'r') as f:
        feature_data = json.load(f)


    num_of_feats = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    for n in num_of_feats:
        print(f'num of feats: {n}')
        feature_list_sig_pearson = {}
        feature_list_sig_spearman = {}
        phon_groups = itertools.combinations(PHON_FEATURES, n)
        morph_groups = itertools.combinations(MORPH_FEATURES, n)

        phons = []
        morphs = []

        for i in phon_groups:
            phons.append(i)

        for i in morph_groups:
            morphs.append(i)

        for i in phons:
            inner = 0
            for j in morphs:
                inner +=1
                combined = i + j
                intersect = None
                for f in combined:
                    if intersect is None:
                        intersect = set(feature_data[f])
                    else:
                        intersect = set.intersection(intersect, set(feature_data[f]))
                
                pearson, spearman = calculate_significance(i, j, data, intersect)

                pval_pear = pearson[1]
                pval_spear = spearman[1]

                combined = str(combined)

                if pval_pear < 0.05:
                    feature_list_sig_pearson[combined] = pearson
                if pval_spear < 0.05:
                    feature_list_sig_spearman[combined] = spearman
            
        sorted_spear = sorted(feature_list_sig_spearman, key=lambda x: feature_list_sig_spearman[x][0])
        sorted_spear_dict = {}
        for combo in sorted_spear:
            sorted_spear_dict[combo] = feature_list_sig_spearman[combo]

        sorted_pear = sorted(feature_list_sig_pearson, key=lambda x: feature_list_sig_pearson[x][0])
        sorted_pear_dict = {}
        for combo in sorted_pear:
            sorted_pear_dict[combo] = feature_list_sig_pearson[combo]


        spear_output = f"spearman_significant/feature_list_{n}.json"
        pear_output = f"pearson_significant/feature_list_{n}.json"

        with open(spear_output, 'w') as f:
            json.dump(sorted_spear_dict, f)
        
        with open(pear_output, 'w') as f:
            json.dump(sorted_pear_dict, f)
        
        print('dumped')



main()