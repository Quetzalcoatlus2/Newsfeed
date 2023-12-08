import requests
#import tkinter as tk
from requests.exceptions import RequestException
from newsapi import NewsApiClient
#from tkinter import ttk, scrolledtext

newsapi = NewsApiClient(api_key='33064a07856d4cf98dd5fd5d759d3ef4')

def get_articles(apiKey, language, country, category, pageSize, q, sources):
    newsapi_url = 'https://newsapi.org/v2/top-headlines'
    parameters = {
        'apiKey': apiKey,
        'language': language,
        'country': country,
        'category': category,
        'pageSize': pageSize,
        'q': q,
        'sources': sources
    }

    try:
        response = requests.get(newsapi_url, parameters)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        return response.json()['articles']
    except RequestException as e:
        print(f"Network error: {e}")
        return None

    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"ERROR {response.status_code}: {response.text}")
        return None
    

#def display_articles_gui(articles):
    root = tk.Tk()
    root.title("News Articles")

    for i, article in enumerate(articles, start=1):
        frame = ttk.Frame(root, padding="10")
        frame.grid(row=i, sticky=(tk.W, tk.E))

        title = ttk.Label(frame, text=f"#{i} {article['title']}", font=("Verdana", 10))
        title.grid(row=0, column=0, sticky=(tk.W))

        source = ttk.Label(frame, text=f"Source: {article['source']['name']}", font=("Arial", 12))
        source.grid(row=1, column=0, sticky=(tk.W))

        url = ttk.Label(frame, text=f"URL: {article['url']}", font=("Arial", 12))
        url.grid(row=2, column=0, sticky=(tk.W))

    root.mainloop()

def display_articles(articles):
    if articles:
        for i, article in enumerate(articles, start = 1):
            print(f"#{i} {article['title']}")
            print(f"   Article source: {article['source']['name']}")
            print(f"   Link: {article['url']}")
            print("\n")
    else:
        print("No articles found. Try again.")

if __name__ == "__main__":
    # API key source: https://newsapi.org/
    apiKey = '33064a07856d4cf98dd5fd5d759d3ef4'
    
    # For 'country', fill in the country code in uppercase, lowercase, or both (NewsAPI supports 54 countries):
    # ae ar at AU be bg br CA ch cn co cu cz de eg FR GB gr HK hu id ie il IN it jp kr 
    # lt lv ma mx my ng nl no NZ ph pl pt RO rs ru sa se sg si sk th tr tw ua US ve za

    # For 'category', fill in: general, business, entertainment, health, science, sports, technology

    # For 'sources', fill in sources={'google-news', 'bbc-news', 'the-verge'}
    # ATTENTION!!! The "sources" field cannot be mixed with the "country" and "category" fields, so either use sources, or 
    # use "country" + "category"
    articles = get_articles(apiKey, language=None, country= 'ro', category='general', sources=None, pageSize=20, q='hamas')
    display_articles(articles)