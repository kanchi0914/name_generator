import json
import csv

json_list = []
json_data = {}

# CSVファイルのロード
with open('names.csv', 'r') as f:
    # list of dictの作成
    for line in csv.DictReader(f):
        json_list.append(line)

    json_data["players"] = json_list
    print("")

len(json_list)

with open('output2.json', 'w') as f:
    # JSONへの書き込み
    json.dump(json_data, f)

print(json_data['players'][0])