import json
import geojson

PHON_FEATURES = ['1A','2A','3A','4A','6A','7A','8A','9A',
                 '10A','11A','12A','13A','14A','15A','16A',
                 '17A','19A']

MORPH_FEATURES = ['20A','21A','21B','22A','23A','24A','25B'
                  '26A','27A','28A','29A']


def convert_geojson(id, datapoint):
    feat = {}
    feat['type'] = "Feature"
    feat['properties'] = {}

    phon_score = 0
    morph_score = 0
    total_score = 0

    coordinates = [0, 0]
    
    for prop in datapoint:
        if prop in PHON_FEATURES:
            phon_score += datapoint[prop]['value']
            total_score += datapoint[prop]['value']
        elif prop in MORPH_FEATURES:
            morph_score += datapoint[prop]['value']
            total_score += datapoint[prop]['value']
        
        elif prop == "longitude":
            long = datapoint[prop]
            if long < 0:
                coordinates[0] = 359 - long
            else:
                coordinates[0] = long

        elif prop == "latitude":
            coordinates[1] = datapoint[prop]
    
    feat['properties']['phon_score'] = phon_score
    feat['properties']['morph_score'] = morph_score
    feat['properties']['total_score'] = total_score

    feat['geometry'] = {}
    feat['geometry']['type'] = "Point"
    feat['geometry']['coordinates'] = coordinates


    # print(id)
    # print(datapoint)
    feat['id'] = id
    return feat



def main():
    with open('modified_info_standardized.json', 'r') as f:
        complexity_data = json.load(f)

    new_geo = {}
    new_geo['type'] = "FeatureCollection"
    new_geo['features'] = []

    for lang in complexity_data:
        temp = convert_geojson(lang, complexity_data[lang])
        new_geo['features'].append(temp)

    with open('language_data.geojson', 'w') as f:
        geojson.dump(new_geo, f)



main()