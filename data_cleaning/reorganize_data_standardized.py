import json
from sklearn import preprocessing as p
import numpy as np

with open('organized_info.json', 'r') as f:
    data = json.load(f)

for language in data:
    removal = []

    for item in data[language]:
        #4A (Voicing in Plosives and Fricatives)
        if item == "4A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 4:
                data[language][item]['value'] = 2

        #6A(Uvular Consonants)
        elif item == "6A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 4:
                data[language][item]['value'] = 2


        # 7A Glottalized consonants
        elif item == "7A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2 or data[language][item]['value'] == 3 or data[language][item]['value'] == 4:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 5 or data[language][item]['value'] == 6 or data[language][item]['value'] == 7:
                data[language][item]['value'] = 2

            elif data[language][item]['value'] == 8:
                data[language][item]['value'] = 3

        #8A
        elif item == "8A":
            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 4:
                data[language][item]['value'] = 3

            elif data[language][item]['value'] == 5:
                data[language][item]['value'] = 2
            
        #9A (The Velar Nasal)
        elif item == "9A":

            if data[language][item]['value'] == 3:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 1:
                data[language][item]['value'] = 2

        #11A (Front Rounded Vowels)
        elif item == "11A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 4:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 2


        #13A  (Tone)
        elif item == "13A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 2


        #19A (Presence of Uncommon Consonants)
        elif item == "19A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2 or data[language][item]['value'] == 3 or data[language][item]['value'] == 4 or data[language][item]['value'] == 5:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 7:
                data[language][item]['value'] = 2
                
            elif data[language][item]['value'] == 6:
                data[language][item]['value'] = 3


        #20A (Fusion of Selected Inflectional Formatives)
        elif item == "20A":

            if data[language][item]['value'] == 1 or data[language][item]['value'] == 2 or data[language][item]['value'] == 3:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 4 or data[language][item]['value'] == 5 or data[language][item]['value'] == 6 or data[language][item]['value'] == 7:
                data[language][item]['value'] = 2


        #21A (Exponence of Selected Inflectional Formatives)
        elif item == "21A":
            # no case
            if data[language][item]['value'] == 5:
                data[language][item]['value'] = 0
            # single
            elif data[language][item]['value'] == 1:
                data[language][item]['value'] = 1
            #double combo
            elif data[language][item]['value'] == 2 or data[language][item]['value'] == 3 or data[language][item]['value'] == 4:
                data[language][item]['value'] = 2


        #21B (Exponence of Tense-Aspect-Mood Inflection)
        elif item == "21B":

            if data[language][item]['value'] == 6:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 1:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 2 or data[language][item]['value'] == 5:
                data[language][item]['value'] = 2

            elif data[language][item]['value'] == 3 or data[language][item]['value'] == 4:
                data[language][item]['value'] = 3


        #23A Locus of Marking in the Clause
        elif item == "23A":

            if data[language][item]['value'] == 4:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 1 or data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 2

            elif data[language][item]['value'] == 5:
                removal.append(item)


        # 24A(Locus of Marking in Possessive Noun Phrases)
        elif item == "24A":

            if data[language][item]['value'] == 4:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 1 or data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 2

            elif data[language][item]['value'] == 5:
                removal.append(item)


        #25B Zero Marking of A and P Arguments
        elif item == "25B":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1


        #26A Prefixing vs. Suffixing in Inflectional Morphology
        elif item == "26A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 2

            elif data[language][item]['value'] == 6:
                data[language][item]['value'] = 2

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 3

            elif data[language][item]['value'] == 5:
                data[language][item]['value'] = 3

            elif data[language][item]['value'] == 4:
                data[language][item]['value'] = 4


        #27A (Reduplication)
        elif item == "27A":

            if data[language][item]['value'] == 3:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 1:
                data[language][item]['value'] = 2


        #28A Case syncretism
        elif item == "28A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 2

            elif data[language][item]['value'] == 4:
                data[language][item]['value'] = 3


        #29A (Reduplication)
        elif item == "29A":

            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0

            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1

            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 2

        elif item[0].isdigit():
            data[language][item]['value'] -= 1

    for feat in removal:
        data[language].pop(feat)

#normalizing

features = ('1A', '2A', '3A', '4A', '6A', '7A', '8A', '9A','11A', '13A','19A','20A', '21A', '21B', '22A', '23A', '24A', '25A','25B', '26A','27A', '28A', '29A')
feature_values = {}
for language in data:
    for feat in data[language]:
        if feat not in features:
            continue
        if feat not in feature_values:
            feature_values[feat] = []
        feature_values[feat].append(data[language][feat]['value'])

for feat in feature_values:
    arr = np.array(feature_values[feat]).reshape(-1, 1)
    normalized = p.MinMaxScaler().fit_transform(arr)
    i = 0
    for language in data:
        if feat in data[language]:
            data[language][feat]['value'] = normalized[i, 0]
            i += 1

with open('modified_info_standardized.json', 'w') as f:
    json.dump(data, f)
