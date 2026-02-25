import os
import csv
import json
import pandas as pd

bad = ".DS_Store"
directory = "datasets"
all_info = {}

file_list = ['1A.tsv', '2A.tsv', '3A.tsv', '4A.tsv', '5A.tsv', '6A.tsv', '7A.tsv', '8A.tsv', '9A.tsv', '10A.tsv', '10B.tsv', '11A.tsv', '12A.tsv', '13A.tsv', '14A.tsv', '15A.tsv', '16A.tsv', '17A.tsv', '18A.tsv', '19A.tsv', '20A.tsv', '21A.tsv', '21B.tsv', '22A.tsv', '23A.tsv', '24A.tsv', '25A.tsv', '25B.tsv', '26A.tsv', '27A.tsv', '28A.tsv', '29A.tsv']

for file in file_list:
    path = f"{directory}/{file}"
    print(file)

    data_name = file[:file.find('.')]

    data = pd.read_csv(path, sep='\t')
    data = data.to_dict('index')
    for index in data:
        info = data[index]
        code = info['wals code']
        name = info['name']
        value = info['value']
        description = info['description']
        if type(description) != str:
            description = "Nan"
        lat = info['latitude']
        long = info['longitude']
        genus = info['genus']
        family = info['family']
        area = info['area']

        if code not in all_info:
            all_info[code] = {}
            all_info[code]['language_name'] = name
            all_info[code]['latitude'] = lat
            all_info[code]['longitude'] = long
            all_info[code]['genus'] = genus
            all_info[code]['family'] = family
        
        all_info[code][data_name] = {}
        all_info[code][data_name]['value'] = value
        all_info[code][data_name]['description'] = description



with open('organized_info.json', 'w') as f:
    json.dump(all_info, f)

data = pd.DataFrame(all_info)
data = data.transpose()

data.to_csv('organized_info.csv')
