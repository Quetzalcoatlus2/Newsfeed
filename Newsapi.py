import requests
import tkinter as tk
from requests.exceptions import RequestException
from newsapi import NewsApiClient
from tkinter import ttk, Label, Button, Entry, Frame, Text, Scrollbar, Canvas, W, E, N, S
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser

newsapi = NewsApiClient(api_key='33064a07856d4cf98dd5fd5d759d3ef4')

previous_window = None

def open_url(event, url):
    webbrowser.open(url)

def buttons(i):
    L1 = Label(window, text = 'Cuvânt cheie:')
    L1.grid(row = i, sticky = W)
    E1 = Entry(window, bd=5)
    E1.grid(row = i, padx = 80, sticky = W)
    button = Button(window, text = "Căutare", command = lambda: keyword_articles(E1.get()))
    button.grid(row = i, padx = 220, sticky = W)
    L2 = Label(window, text = f"Număr rezultate:{totalResults}")
    L2.grid(row=i+1, sticky=(W)) 

def get_articles(apiKey, language, country, category, pageSize, q, sources):
    newsapi_url = 'https://newsapi.org/v2/top-headlines'
    parameters = {
        'apiKey': apiKey,
        'language': language,
        'country': country,
        'category': category,
        'pageSize': pageSize,
        'q': q,
        'sources': ','.join(sources) if sources else None
    }

    global totalResults
    articles = None
    error = None
    status = None
    code = None
    message = None

    try:
        response = requests.get(newsapi_url, parameters)
        response.raise_for_status()
        articles = response.json()['articles']
        totalResults = response.json()['totalResults']
        status = response.json()['status']
    except RequestException as e:
        print(f"Network error: {e}")
        error = e

    if response.status_code == 200:
        return articles, totalResults, None, None, None, None
    else:
        status = response.json()['status']
        print(f"Status: {status}")
        code = response.json()['code']
        print(f"Code: {code}")
        message = response.json()['message']
        print(f"Message: {message}")
        return None, None, error, status, code, message

def keyword_articles(E1):
    global totalResults
    articles, totalResults, error, status, code, message = get_articles(apiKey, language='en', country=None, category=None, sources=None , pageSize=2, q=f'{E1}')    
    display_articles_gui(articles, error, status, code, message)

def exit_fullscreen(event):
    window.attributes('-fullscreen', False)

def display_articles_gui(articles, error, status, code, message):

    global previous_window
    global window

    if previous_window is not None:
        previous_window.destroy()

    window = tk.Tk()
    window.title("Articole")
    #window.attributes('-fullscreen', True)
    #window.bind('<Escape>', exit_fullscreen)

    canvas = Canvas(window)
    scrollbar = Scrollbar(window, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set) 
    frame = Frame(canvas)
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    # canvas.grid(row=0, column=0, sticky=(N, S, E, W))
    # scrollbar.grid(row=0, column=1, sticky=(N, S))
    canvas.create_window((0, 0), window=frame, anchor='nw')

    if articles:
        for i, article in enumerate(articles, start=1):
            article_frame = Frame(frame, padx=10)
            article_frame.grid(row=i, sticky=(W, E))

            title_label = Label(article_frame, text=f"#{i} {article['title']}", font=("Verdana", 10))
            title_label.grid(row=0, sticky=(W))

            source_label = Label(article_frame, text=f"Sursă: {article['source']['name']}", font=("Arial", 12))
            source_label.grid(row=1, sticky=(W))

            author_label = Label(article_frame, text=f"Autori: {article['author']}", font=("Arial", 12))
            author_label.grid(row=2, sticky=(W))

            description_label = Label(article_frame, text=f"Scurtă descriere: {article['description']}", font=("Arial", 12))
            description_label.grid(row=3, sticky=(W))

            publishedAt_label = Label(article_frame, text=f"Publicat la: {article['publishedAt']}", font=("Arial", 12))
            publishedAt_label.grid(row=7, sticky=(W))

            url_label = Label(article_frame, text=f"Link: {article['url']}", font=("Arial", 12), fg="blue", cursor="hand2")
            url_label.grid(row=4, sticky=(W))
            url_label.bind("<Button-1>", lambda event, url=article['url']: open_url(event, url))

            urlToImage_label = Label(article_frame, text=f"Link imagine: {article['urlToImage']}", font=("Arial", 12), fg="blue", cursor="hand2")
            urlToImage_label.grid(row=5, sticky=(W))
            urlToImage_label.bind("<Button-1>", lambda event, url=article['urlToImage']: open_url(event, url))

            
            response = requests.get(article['urlToImage'])
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            photo = ImageTk.PhotoImage(img)

            
            img_label = Label(article_frame, image=photo)
            img_label.image = photo 
            img_label.grid(row=6, sticky=(W))

           

        buttons(i+1)

    elif error:
        error = Label(window, text=f"Network error: {error}", font=("Arial", 12))
        error.grid(row=1, column=0, sticky=(W))
        status = Label(window, text=f"Status: {status}", font=("Arial", 12))
        status.grid(row=2, column=0, sticky=(W))
        code = Label(window, text=f"Cod: {code}", font=("Arial", 12))
        code.grid(row=3, column=0, sticky=(W))
        message = Label(window, text=f"Mesaj: {message}", font=("Arial", 12))
        message.grid(row=4, column=0, sticky=(W))
        buttons(5)

    else:
        no_articles = Label(window, text="Nu s-au găsit articole. Încercați din nou.", font=("Arial", 12))
        no_articles.grid(row=0, column=0, sticky=(W))
        buttons(1)
    
    window.update()
    canvas.configure(scrollregion=canvas.bbox('all'))

    previous_window = window
    window.mainloop()

if __name__ == "__main__":
    apiKey = '33064a07856d4cf98dd5fd5d759d3ef4'
    articles, totalResults, error, status, code, message = get_articles(apiKey, language='en', country=None, category= None, sources=None , pageSize=2, q=None)    
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