import json

import numpy as np
import xml.etree.ElementTree as ET
from collections import Counter


def handler(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row
        root = ET.fromstring(text)
        clothing_items = []

        for clothing_element in root.findall('clothing'):
            item_data = {
                'id': int(clothing_element.find('id').text.strip()),
                'name': clothing_element.find('name').text.strip(),
                'category': clothing_element.find('category').text.strip(),
                'size': clothing_element.find('size').text.strip(),
                'color': clothing_element.find('color').text.strip(),
                'material': clothing_element.find('material').text.strip(),
                'price': int(clothing_element.find('price').text.strip()),
                'rating': float(clothing_element.find('rating').text.strip()),
                'reviews': int(clothing_element.find('reviews').text.strip())
            }

            exclusive_element = clothing_element.find('exclusive')
            sporty_element = clothing_element.find('sporty')
            new_element = clothing_element.find('new')

            if exclusive_element is not None:
                item_data['exclusive'] = True if exclusive_element.text.strip() == "yes" else False

            if sporty_element is not None:
                item_data['sporty'] = True if sporty_element.text.strip() == "yes" else False

            if new_element is not None:
                item_data['new'] = True if new_element.text.strip() == "+" else False

            clothing_items.append(item_data)
        return clothing_items


items = []
for i in range(1, 100):
    file_name = f"data/{i}.xml"
    items += handler(file_name)

with open("4_result_all.json", 'w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(sorted(items, key=lambda x: x['id'], reverse=True), ensure_ascii=False, indent=2))

with open('4_filtered_result.json', 'w', encoding='utf-8') as json_file:
    filtered_items = []
    for cloth in items:
        if cloth['color'].find('Фиолетовый') != -1:
            filtered_items.append(cloth)
    json.dump(filtered_items, json_file, ensure_ascii=False, indent=2)

price_stat = {}
price_values = [item['price'] for item in items]
price_stat['sum'] = int(np.sum(price_values))
price_stat['min'] = int(np.min(price_values))
price_stat['max'] = int(np.max(price_values))
price_stat['avg'] = float(np.mean(price_values))

size_values = [item['size'] for item in items]
size_stat = Counter(size_values)

result_data = {
    'price_stat': price_stat,
    'size_stat': size_stat
}

with open('4_stats.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_data, json_file, ensure_ascii=False, indent=2)