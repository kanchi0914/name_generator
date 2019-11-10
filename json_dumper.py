import json, csv

def convert(path):
    json_list = []

    with open(path, 'r') as f:
        for row in csv.DictReader(f):
            json_list.append(row)

    with open('output.json', 'w') as f:
        json.dump(json_list, f)


def load():
    with open('output.json', 'r') as f:
        return json.load(f)
