from bs4 import BeautifulSoup
import requests
import pandas as pd
matrice = []


url = "https://www.bbc.com/search?q=social+inequality&page="

for i in range(176) : 
    newurl = url + str(i)
    response = requests.get(newurl)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    elements = soup.find_all("div", attrs={"data-testid": "newport-card"})
    for j in elements : 
        liste = []
        article_url = j.find("a")
        article_url = ("https://www.bbc.com/"+article_url['href'])
        if "news" not in article_url : 
            continue 
        element = j.find("span", class_="sc-6fba5bd4-1 efYorw")
        date = element.text
        response = requests.get(article_url)
        content = response.text
        soup_article = BeautifulSoup(content, "html.parser")
        soup_article = soup_article.find("div", class_="sc-4b0aaa-0 dGavUm")
        print(article_url)
        print(date)
        try:
            soup_article = soup_article.select("a")
        except Exception as e:
            soup_article = ["no_topics"] 
        for k in range(len(soup_article)) : 
            if soup_article[k] != "no_topics" : 
                soup_article[k] = soup_article[k].text
        liste = [article_url,date,soup_article]
        matrice.append(liste)

df = pd.DataFrame(matrice, columns=["url", "date", "topics"])

df.to_csv("articles_bbc.csv")