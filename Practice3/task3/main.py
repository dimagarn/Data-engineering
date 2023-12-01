import json

import numpy as np
import xml.etree.ElementTree as ET
from collections import Counter


def handler(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row
        item = dict()
        root = ET.fromstring(text)
        item["name"] = root.find("name").text.strip()
        item["constellation"] = root.find("constellation").text.strip()
        item["spectral_class"] = root.find("spectral-class").text.strip()
        item["radius"] = int(root.find("radius").text.strip())
        item["rotation"] = float(root.find("rotation").text.strip().split()[0])
        item["age"] = float(root.find("age").text.strip().split()[0])
        item["distance"] = float(root.find("distance").text.strip().split()[0])
        item["absolute_magnitude"] = float(root.find("absolute-magnitude").text.strip().split()[0])
        return item


items = []
for i in range(1, 500):
    file_name = f"data/{i}.xml"
    items.append(handler(file_name))

with open("3_result_all.json", "w", encoding="utf-8") as json_file:
    json_file.write(json.dumps(sorted(items, key=lambda x: x["age"], reverse=True), ensure_ascii=False, indent=2))

filtered_items = [item for item in items if item["constellation"] == "Дева"]
with open("3_filtered_result.json", "w", encoding="utf-8") as json_file:
    json.dump(filtered_items, json_file, ensure_ascii=False, indent=2)

age_stat = {}
age_values = [item["age"] for item in items]
age_stat["sum"] = int(np.sum(age_values))
age_stat["min"] = int(np.min(age_values))
age_stat["max"] = int(np.max(age_values))
age_stat["avg"] = float(np.mean(age_values))

constellation_values = [item["constellation"] for item in items]
constellation_stat = Counter(constellation_values)

result_data = {
    "age_stat": age_stat,
    "constellation_stat": constellation_stat
}

with open("3_stats.json", "w", encoding="utf-8") as json_file:
    json.dump(result_data, json_file, ensure_ascii=False, indent=2)
