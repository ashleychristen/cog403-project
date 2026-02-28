import json

with open('modified_info.json', 'r') as f:
    data = json.load(f)

db = ['1A', '2A', '3A', '4A', '5A', '6A', '7A', '8A', '9A', '10A', '11A', '12A', '13A', '14A', '15A', '16A', '17A', '18A', '19A', '20A', '21A', '21B', '22A', '23A', '24A', '25A', '25B', '26A', '27A', '28A', '29A']

features = {}

for language in data:
    for item in data[language]:
        if item in db:
            
            if item not in features:
                features[item] = []
            
            features[item].append(language)

with open('modified_feature_list.json', 'w') as f:
    json.dump(features, f)