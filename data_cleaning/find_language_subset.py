import json
import itertools


PHON_FEATURES = ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','15A','16A',
                 '17A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A','25B',
                  '26A','27A','28A','29A']

# print('phon features =', len(PHON_FEATURES))
# print('morph features =', len(MORPH_FEATURES))


filepath = 'modified_feature_list.json'

with open(filepath) as f:
    data = json.load(f)

num_of_feats = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for n in num_of_feats:
    feature_list_counts = {}
    phon_groups = itertools.combinations(PHON_FEATURES, n)
    morph_groups = itertools.combinations(MORPH_FEATURES, n)

    phons = []
    morphs = []

    for i in phon_groups:
        phons.append(i)

    for i in morph_groups:
        morphs.append(i)

    # print(len(phons))
    # print(len(morphs))

    count = 0
    for i in phons:
        inner = 0
        for j in morphs:
            inner +=1
            combined = i + j
            intersect = None
            for f in combined:
                if intersect is None:
                    intersect = set(data[f])
                else:
                    intersect = set.intersection(intersect, set(data[f]))
            
            feature_list_counts[combined] = intersect
            # print(combined)
        # print(i)
        # print(count, inner)
        count += 1

# print(feature_list_counts.keys())
# feature_list_counts = sorted(feature_list_counts, key=lambda x: len(feature_list_counts[x]), reverse=True)
# print(feature_list_counts)

    max = 0
    max_list = ""
    for feats in feature_list_counts:
        if len(feature_list_counts[feats]) > max:
            max = len(feature_list_counts[feats])
            max_list = feats
    print('num of feats =', n)
    print(max, max_list)
