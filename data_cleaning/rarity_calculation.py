import json

with open('modified_info.json', 'r') as f:
    data = json.load(f)

features = {}
for lang in data:
    for feat in data[lang]:
        if feat[0].isdigit():

            if feat not in features:
                features[feat] = []
            
            features[feat].append(data[lang][feat]['value'])

# print(features)

features_rarity = {}
for feat in features:
    sort = sorted(features[feat], reverse=True)
    # print(sort)
    features[feat] = sort
    
    highest = max(sort)
    rarity = sort.count(highest) / len(sort)
    
    features_rarity[feat] = rarity

print(features_rarity)