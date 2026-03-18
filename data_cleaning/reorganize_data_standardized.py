import json
from sklearn import preprocessing as p
import numpy as np

with open('organized_info.json', 'r') as f:
    data = json.load(f)

features_to_remove = ["10B", "5A", "18A", "25A"]

for language in data:
    removal = []

    for item in data[language]:
        if not item[0].isnumeric():
            continue
 
        value = data[language][item]['value']

        if item in features_to_remove:
            removal.append(item)
            continue
        
        #4A (Voicing in Plosives and Fricatives)
        if item == "4A":

            if value == 1:
                value = 0

            elif value == 2:
                value = 1

            elif value == 3:
                value = 1

            elif value == 4:
                value = 2

        #6A(Uvular Consonants)
        elif item == "6A":

            if value == 1:
                value = 0

            elif value == 2:
                value = 1

            elif value == 3:
                value = 1

            elif value == 4:
                value = 2


        # 7A Glottalized consonants
        elif item == "7A":

            if value == 1:
                value = 0

            elif value == 2 or value == 3 or value == 4:
                value = 1

            elif value == 5 or value == 6 or value == 7:
                value = 2

            elif value == 8:
                value = 3

        #8A
        elif item == "8A":
            if value == 1:
                value = 0

            elif value == 2:
                value = 1

            elif value == 3:
                value = 1

            elif value == 4:
                value = 3

            elif value == 5:
                value = 2
            
        #9A (The Velar Nasal)
        elif item == "9A":

            if value == 3:
                value = 0

            elif value == 2:
                value = 1

            elif value == 1:
                value = 2

        #10A (Vowel Nasalization)
        elif item == "10A":
            if value == 1:
                value = 0
            elif value == 2:
                value = 1
            
        #11A (Front Rounded Vowels)
        elif item == "11A":

            if value == 1:
                value = 0

            elif value == 3:
                value = 1

            elif value == 4:
                value = 1

            elif value == 2:
                value = 2

        #13A  (Tone)
        elif item == "13A":

            if value == 1:
                value = 0

            elif value == 2:
                value = 1

            elif value == 3:
                value = 2

        #14A (Fixed Stress Locations)
        elif item =="14A":
            if value == 1:
                value = 0

            elif value == 2 or value == 3 or value == 4 or value == 5 or value == 6 or value == 7:
                value = 1

        #15A (Weight-Sensitive Stress)
        elif item =="15A":
            if value == 1 or value == 2 or value == 3 or value == 4:
                value = 2

            elif value == 5:
                value = 3

            elif value == 6:
                value = 5

            elif value == 7:
                value = 3

            elif value == 8:
                value = 1

        #16A (Weight Factors in Weight-Sensitive Stress Systems)
        elif item =="16A":
            if value == 1: 
                value = 0

            elif value == 2 or value == 3 or value == 5:
                value = 1

            elif value == 4 or value == 6:
                value = 2

            elif value == 7:
                value = 2.5

        #17A (Rhythm Types)
        elif item =="17A":
            if value == 1 or value == 2: 
                value = 1

            elif value == 3:
                value = 2

            elif value == 4 or value == 5:
                value = 0

        #19A (Presence of Uncommon Consonants)
        elif item == "19A":

            if value == 1:
                value = 0

            elif value == 2 or value == 3 or value == 4 or value == 5:
                value = 1

            elif value == 7:
                value = 2
                
            elif value == 6:
                value = 3

        #MORPHOLOGY

        #20A (Fusion of Selected Inflectional Formatives)
        elif item == "20A":

            if value == 1 or value == 2 :
                value = 1

            elif value == 3 or value == 7:
                value = 2

            elif value == 4 or value == 5 or value == 6:
                value = 3


        #21A (Exponence of Selected Inflectional Formatives)
        elif item == "21A":
            # no case
            if value == 5:
                value = 0
            # single
            elif value == 1:
                value = 1
            #double combo
            elif value == 2 or value == 3 or value == 4:
                value = 2


        #21B (Exponence of Tense-Aspect-Mood Inflection)
        elif item == "21B":

            if value == 6:
                value = 0

            elif value == 1:
                value = 1

            elif value == 2 or value == 5:
                value = 2

            elif value == 3 or value == 4:
                value = 3


        #23A Locus of Marking in the Clause
        elif item == "23A":

            if value == 4:
                value = 0

            elif value == 1 or value == 2:
                value = 1

            elif value == 3:
                value = 2

            elif value == 5:
                removal.append(item)


        # 24A(Locus of Marking in Possessive Noun Phrases)
        elif item == "24A":

            if value == 4:
                value = 0

            elif value == 1 or value == 2:
                value = 1

            elif value == 3:
                value = 2

            elif value == 5:
                removal.append(item)


        #25B Zero Marking of A and P Arguments
        elif item == "25B":

            if value == 1:
                value = 0

            elif value == 2:
                value = 1


        #26A Prefixing vs. Suffixing in Inflectional Morphology
        elif item == "26A":

            if value == 1:
                value = 1

            elif value == 2:
                value = 2

            elif value == 6:
                value = 2

            elif value == 3:
                value = 3

            elif value == 5:
                value = 3

            elif value == 4:
                value = 4


        #27A (Reduplication)
        elif item == "27A":

            if value == 3:
                value = 0

            elif value == 2:
                value = 1

            elif value == 1:
                value = 2


        #28A Case syncretism
        elif item == "28A":

            if value == 1:
                value = 0

            elif value == 2:
                value = 1

            elif value == 3:
                value = 2

            elif value == 4:
                value = 3


        #29A (Reduplication)
        elif item == "29A":

            if value == 1:
                value = 0

            elif value == 2:
                value = 1

            elif value == 3:
                value = 2
        data[language][item]['value'] = value
    for feat in removal:
        data[language].pop(feat)

#normalizing

features = ('1A', '2A', '3A', '4A', '6A', '7A', '8A', '9A', '10A', '11A', '12A', '13A', '14A', '15A', '16A', '17A','19A','20A', '21A', '21B', '22A', '23A', '24A','25B', '26A','27A', '28A', '29A')
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
            data[language][feat]['value'] = round(float(normalized[i,0]),3)
            i += 1

with open('modified_info_standardized.json', 'w') as f:
    json.dump(data, f)
