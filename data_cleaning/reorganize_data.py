import json

with open('organized_info.json', 'r') as f:
    data = json.load(f)

for language in data:
    removal = []

    for item in data[language]:
        if item == "4A":
            if data[language][item]['value'] == 3:
                data[language][item]['value'] = 2
            elif data[language][item]['value'] == 4:
                data[language][item]['value'] = 3
        
        elif item == "6A":
            if data[language][item]['value'] == 3:
                data[language][item]['value'] = 2
            elif data[language][item]['value'] == 4:
                data[language][item]['value'] = 3
        
        elif item == "7A":
            if data[language][item]['value'] == 1:
                data[language][item]['value'] = 0
            elif data[language][item]['value'] == 2 or data[language][item]['value'] == 3 or data[language][item]['value'] == 4:
                data[language][item]['value'] = 1
            elif data[language][item]['value'] == 5 or data[language][item]['value'] == 6 or data[language][item]['value'] == 7:
                data[language][item]['value'] = 2
            elif data[language][item]['value'] == 8:
                data[language][item]['value'] = 3
        
        elif item == "23A" or item == "24A" or item == "25A":
            if data[language][item]['value'] == 4:
                data[language][item]['value'] = 0
            elif data[language][item]['value'] == 2:
                data[language][item]['value'] = 1
            elif data[language][item]['value'] == 3:
                data[language][item]['value'] = 2
            elif data[language][item]['value'] == 5: # removing other to avoid inconsistency
                removal.append(item)
        
        elif item == "26A":
            print('26A')

        elif item[0].isnumeric():
            data[language][item]['value'] -= 1
        
    for feat in removal:
        data[language].pop(feat)



with open('modified_info.json', 'w') as f:
    json.dump(data, f)


