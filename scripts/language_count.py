import json

both = ('1A', '3A', '4A', '6A', '7A', '8A', '9A', '11A', '13A', '14A', '16A', '20A', '21A', '21B', '22A', '23A', '24A', '25B', '26A', '27A', '28A', '29A')

with open('cleaned_data/modified_info_standardized.json', 'r') as f:
    data = json.load(f)

chosen_languages = []
for language in data:

    same = 0

    feats = data[language].keys()
    for f in both:
        if f in feats:
            same += 1
    
    if same == len(both):

        chosen_languages.append(language)

print(len(chosen_languages))