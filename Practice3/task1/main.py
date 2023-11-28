from bs4 import BeautifulSoup
import re
import json


def handle_file(file_name):
    with open(file_name, encoding="UTF-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, "html.parser")

        item = dict()
        item["category"] = site.find_all("span", string=re.compile("Категория:"))[0].get_text().replace("Категория:", "").strip()
        item["title"] = site.find_all("h1")[0].get_text().strip()
        item["author"] = site.find_all("p", attrs={'class': "author-p"})[0].get_text().strip()
        item["pages"] = int(site.find_all("span", string=re.compile("Объем:"))[0].get_text().replace("Объем:", "").replace("страниц", "").strip())
        item["year"] = int(site.find_all("span", attrs={'class': "year"})[0].get_text().replace("Издано в", "").strip())
        item["ISBN"] = site.find_all("span", string=re.compile("ISBN:"))[0].get_text().replace("ISBN:", "").strip()
        item["description"] = site.find_all("p", string=re.compile("Описание"))[0].get_text().replace("Описание", "").strip()
        item["img_link"] = site.find("img")["src"]
        item["rating"] = float(site.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().replace("Рейтинг:", "").strip())
        item["views"] = site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().replace("Просмотры:", "").strip()

        return item

min = handle_file("1.html")["rating"]
max = min
sum = 0
count = 0
items = []
for i in range(1, 999):
    file_name = f"{i}.html"
    result = handle_file(file_name)
    items.append(result)

    if min > result["rating"]:
        min = result["rating"]
    if max < result["rating"]:
        max = result["rating"]
    if result["category"] == "роман":
        count += 1
    sum += result["rating"]
avr = sum / len(items)

items = sorted(items, key=lambda x: x["views"], reverse=True)
with open("result_all_1.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []
for book in items:
    if book["rating"] >= 4:
        filtered_items.append(book)

print("Количество книг:", len(items))
print("Количество книг с рейтингом выше 4:", len(filtered_items))
print("Частота метки категории роман:", count)

statistic = dict()

statistic["Минимальный рейтинг"] = min
statistic["Максимальный рейтинг"] = max
statistic["Суммарный рейтинг"] = sum
statistic["Средний рейтинг"] = avr

with open("stat_1.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(statistic, ensure_ascii=False))
