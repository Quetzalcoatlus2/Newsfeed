#Implementați o aplicație GUI cu ajutorul căreia utilizatorul poate să vizioneze cele mai recente news feeds legat de 
#un anume subiect. Informațiile ar trebui să provină din diverse surse (cel puțin 4 surse), de preferat folosindu-se 
#API-urile puse la dispoziție de platformele respective (Reddit, BBc, Google News, etc.). Pentru partea de GUI se poate 
#folosi tkinter sau alte biblioteci asemănătoare.

import requests
import tkinter as tk
from requests.exceptions import RequestException
from newsapi import NewsApiClient
from tkinter import *

newsapi = NewsApiClient(api_key='33064a07856d4cf98dd5fd5d759d3ef4')




def get_articles(apiKey, language, country, category, pageSize, q, sources):
    newsapi_url = 'https://newsapi.org/v2/top-headlines'
    parameters = {
        'apiKey': apiKey, # '33064a07856d4cf98dd5fd5d759d3ef4
        'language': language,
        'country': country,
        'category': category,
        'pageSize': pageSize,
        'q': q,
        'sources': ','.join(sources) if sources else None
    }

    articles = None
    error = None
    number_results = None
    status = None
    code = None
    message = None

    try:
        response = requests.get(newsapi_url, parameters)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        articles = response.json()['articles']
        number_results = response.json()['totalResults']
        status = response.json()['status']
        status_code = response.status_code
    except RequestException as e:
        print(f"Network error: {e}")
        error = e
        

    if response.status_code == 200:
        return articles, None, None, None, None, None
    else:
        
        status = response.json()['status']
        print(f"Status: {status}")
        code = response.json()['code']
        print(f"Code: {code}")
        message = response.json()['message']
        print(f"Message: {message}")
        return None, error, status, code, message
    
def keyword_articles(E1):
    articles, error, status, code, message, status_code = get_articles(apiKey, language='en', country=None, category=None, sources=None , pageSize=5, q=f'{E1}')    
    display_articles_gui(articles, error, status, code, message)

previous_window = None

def display_articles_gui(articles, error, status, code, message):
    global previous_window
    if previous_window is not None:
        previous_window.destroy()
    window = tk.Tk()
    window.title("Articole")
    if articles:
        for i, article in enumerate(articles, start=1):
             frame = Frame(window, padx=10)
             frame.grid(row=i+2, sticky=(W, E))

             title = Label(frame, text=f"#{i} {article['title']}", font=("Verdana", 10))
             title.grid(row=0, column=0, sticky=(W))

             source = Label(frame, text=f"Sursă: {article['source']['name']}", font=("Arial", 12))
             source.grid(row=1, column=0, sticky=(W))

             author = Label(frame, text=f"Autori: {article['author']}", font=("Arial", 12))
             author.grid(row=2, column=0, sticky=(W))

             description = Label(frame, text=f"Scurtă descriere: {article['description']}", font=("Arial", 12))
             description.grid(row=3, column=0, sticky=(W))

             url = Label(frame, text=f"Link: {article['url']}", font=("Arial", 12))
             url.grid(row=4, column=0, sticky=(W))

             urlToImage = Label(frame, text=f"Link imagine: {article['urlToImage']}", font=("Arial", 12))
             urlToImage.grid(row=5, column=0, sticky=(W))

             publishedAt = Label(frame, text=f"Publicat la: {article['publishedAt']}", font=("Arial", 12))
             publishedAt.grid(row=6, column=0, sticky=(W))

             content = Label(frame, text=f"Conținut articol: {article['content']}", font=("Arial", 12))
             content.grid(row=7, column=0, sticky=(W))


            
           
    else:
        no_articles = Label(window, text="Nu s-au găsit articole. Încercați din nou.", font=("Arial", 12))
        no_articles.grid(row=0, column=0, sticky=(W))
    if  error:
        error = Label(window, text=f"Network error: {error}", font=("Arial", 12))
        error.grid(row=1, column=0, sticky=(W))
        status = Label(window, text=f"Status: {status}", font=("Arial", 12))
        status.grid(row=2, column=0, sticky=(W))
        code = Label(window, text=f"Cod: {code}", font=("Arial", 12))
        code.grid(row=3, column=0, sticky=(W))
        message = Label(window, text=f"Mesaj: {message}", font=("Arial", 12))
        message.grid(row=4, column=0, sticky=(W))
    
    L1 = Label(window, text = 'Cuvânt cheie:')
    L1.grid(row=6, column=0, sticky=(W))
    E1 = Entry(window, bd=5)
    E1.grid(row=7, column=0, sticky=(W))
    button = Button(window, text="Căutare", command=lambda: keyword_articles(E1.get()))
    button.grid(row=8, column=0, sticky=(W))
    previous_window = window
    window.mainloop()


if __name__ == "__main__":
    apiKey = '33064a07856d4cf98dd5fd5d759d3ef'
    articles, error, status, code, message = get_articles(apiKey, language='en', country=None, category=None, sources=None , pageSize=5, q=None)    
    display_articles_gui(articles, error, status, code, message)

    
"""def display_articles(articles):
    if articles:
        for i, article in enumerate(articles, start = 1):
            print(f"#{i} {article['title']}")
            print(f"   Article source: {article['source']['name']}")
            print(f"   Link: {article['url']}")
            print("\n")
    else:
        print("No articles found. Try again.")"""



"""
API key source: https://newsapi.org/
error 401 if API key is invalid or missing

For 'country', fill in the country code in uppercase, lowercase, or both (NewsAPI supports 54 countries):
ae ar at AU be bg br CA ch cn co cu cz de eg FR GB gr HK hu id ie il IN it jp kr 
lt lv ma mx my ng nl no NZ ph pl pt RO rs ru sa se sg si sk th tr tw ua US ve za

For 'category', fill in: general, business, entertainment, health, science, sports, technology

For 'sources', fill in sources={'google-news', 'bbc-news', 'the-verge', 'cnn', 'usa-today', 'abc-news', 
'associated-press', 'axios', 'bloomberg', 'business-insider', 'cbc-news', 'cbs-news', 'cnbc', 'engadget', 
'entertainment-weekly', 'fortune', 'fox-sports', 'google-news-ca', 'google-news-uk', 'hacker-news', 'ign', 
'medical-news-today', 'msnbc', 'mtv-news', 'national-geographic', 'nbc-news', 'news24', 'newsweek', 
'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'politico', 'polygon', 'recode', 'reddit-r-all', 
'reuters', 'techcrunch', 'techradar', 'the-american-conservative', 'the-hill', 'the-huffington-post', 
'the-next-web', 'the-sport-bible', 'the-times-of-india', 'the-washington-times', 'time', 'usa-today', 'vice-news', 
'wired'}
    
 ATTENTION!!! The "sources" field cannot be mixed with the "country" and "category" fields, so either use sources, 
 or use "country" + "category
 """