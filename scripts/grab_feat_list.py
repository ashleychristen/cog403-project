import json

for i in range(1, 12):
    filename = f"pearson_significant/feature_list_{i}.json"
    with open(filename, 'r') as f:
        data = json.load(f)

    for row in data:
        print(i)
        print(row)
        print(data[row])
        break