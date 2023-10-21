import requests
from bs4 import BeautifulSoup
import json

#params = {"limit" : "100"}
#URL = "https://catfact.ninja/facts"
#get = requests.get(URL, params)

str_json = ""
with open("facts.json") as file:
    lines = file.readlines()
    for line in lines:
        str_json += line

data = json.loads(str_json)
data = data['data']

soup = BeautifulSoup("""<table>
    <tr>
        <th>Fact</th>
        <th>Length</th>
    </tr>
</table>""", features="html.parser")

table = soup.contents[0]

for tick in data:
    tr = soup.new_tag("tr")
    for key, val in tick.items():
        td = soup.new_tag("td")
        td.string = str(val)
        tr.append(td)
    table.append(tr)

with open ("task_6.html", "w") as result:
    result.write(soup.prettify())
    result.write("\n")
