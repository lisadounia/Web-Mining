from bs4 import BeautifulSoup
import requests
import pandas as pd


url = "https://en.wikipedia.org/wiki/Social_inequality"
response = requests.get(url)
content = response.text
soup = BeautifulSoup(content, "html.parser")
liens = soup.select("h1")
head = liens[0].text
print(head)
new_head = ""
for i in head : 
    if i ==" " : 
        new_head+= "_"
        continue 
    new_head+= i

new_url = "https://en.wikipedia.org/w/index.php?title="+new_head+"&action=history&offset=&limit=500"
print(new_url)

dico = {}

response = requests.get(new_url)
content = response.text
soup = BeautifulSoup(content, "html.parser")

soup = soup.find(id="pagehistory")

soupliste= soup.select("ul")
for i in soupliste : 
    soup = i.find("bdi")
    soup = soup.find("a")
    print(soup.text)
    url = "https://en.wikipedia.org/" +soup["href"]
    print(url)
    dico[soup.text] = url

df = pd.DataFrame(list(dico.items()), columns=["URL", "dates"])


print(df.head(500))