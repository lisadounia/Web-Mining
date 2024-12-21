import pandas as pd
from bs4 import BeautifulSoup
import requests



df = pd.read_excel("graph/edges.xlsx")

liens = df.iloc[:, 0].tolist()
liens += df.iloc[:, 1].tolist()

liens = list(set(liens))
print(len(liens))
for url in liens : 
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content,"html.parser")
    h1 = soup.select("h1")[0].text
    if h1[-1] == " " :
        h1 = h1[:-1]
    h1final = ""
    for i in h1 : 
        if i == " " : 
            h1final += "_"
            continue
        h1final+=i
    print(h1)
    print(h1final)
    stat_url = "https://pageviews.wmcloud.org/?project=en.wikipedia.org&platform=all-access&agent=user&redirects=0&range=latest-20&pages=Social_inequality"
    print(stat_url)
    response_stat = requests.get(stat_url)
    content_stat = response_stat.text
    soup_stat = BeautifulSoup(content_stat,"html.parser")
    #print(soup_stat.text)
    container = soup.find("div", class_="legend-block legend-block--pages_vues")

    # Étape 2 : Trouver le span avec la classe 'pull-right'
    print(soup_stat.find_all("div", {"class" : "legend-block--body"})[0].text)
