import json
from bs4 import BeautifulSoup
import numpy as np
from collections import Counter


def handler(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row
        items = []
        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all("div", attrs={'class': 'product-item'})
        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = site.find_all("img")[0]["src"]
            item['title'] = site.find_all("span")[0].getText().strip()
            item['price'] = int(site.find_all("price")[0].getText().replace("₽", "").replace(" ", "").strip())
            item['bonus'] = int(
                site.find_all("strong")[0].getText().replace("+ начислим ", "").replace(" бонусов", "").strip())

            props = product.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()
            items.append(item)

        return items


items = []
for i in range(1, 39):
    file_name = f"{i}.html"
    items += handler(file_name)

with open("2_result_all.json", 'w', encoding='utf-8') as file:
    file.write(json.dumps(sorted(items, key=lambda x: x['price'], reverse=True), ensure_ascii=False, indent=2))

with open('2_filtered_result.json', 'w', encoding='utf-8') as json_file:
    filtered_items = []
    for phone in items:
        if phone['title'].find('Samsung') != -1:
            filtered_items.append(phone)
    json.dump(filtered_items, json_file, ensure_ascii=False, indent=2)

bonus_stat = {}
bonus_values = [item['bonus'] for item in items]
bonus_stat['sum'] = int(np.sum(bonus_values))
bonus_stat['min'] = int(np.min(bonus_values))
bonus_stat['max'] = int(np.max(bonus_values))
bonus_stat['avg'] = float(np.mean(bonus_values))

title_values = [item['title'] for item in items]
title_stat = Counter(title_values)

result_data = {
    'bonus_stat': bonus_stat,
    'title_stat': title_stat
}

with open('3 work/task 2/result/2_stats.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_data, json_file, ensure_ascii=False, indent=2)