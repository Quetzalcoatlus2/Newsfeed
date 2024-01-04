from newsapi import NewsApiClient
import requests
from requests.exceptions import RequestException
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser


newsapi = NewsApiClient(api_key='33064a07856d4cf98dd5fd5d759d3ef4')

previous_window = None
totalResults = 0

def open_url(url):
    webbrowser.open(url)


def on_mousewheel(action):
    canvas.yview_scroll(int(-1*(action.delta/80)), "u")


def buttons(i):
    global totalResults
    buttons_frame = tk.Frame(window, padx=10)
    buttons_frame.grid(row=i, sticky=(tk.W, tk.E))

    L1 = tk.Label(buttons_frame, text='Cuvânt cheie:')
    L1.grid(row=0, column=0, sticky=tk.W)
    E1 = tk.Entry(buttons_frame, bd=5)
    E1.grid(row=0, column=1, sticky=tk.W)

    L2 = tk.Label(buttons_frame, text='Introduceți numărul paginii:')
    L2.grid(row=0, column=2, sticky=tk.W)
    E2 = tk.Entry(buttons_frame, bd=5)
    E2.grid(row=0, column=3, sticky=tk.W)

    L3 = tk.Label(buttons_frame, text='Introduceți numărul de rezultate per pagină (20 din oficiu):')
    L3.grid(row=0, column=4, sticky=tk.W)
    E3 = tk.Entry(buttons_frame, bd=5)
    E3.grid(row=0, column=5, sticky=tk.W)

    L4 = tk.Label(buttons_frame, text=f"Număr rezultate:{totalResults}")
    L4.grid(row=1, column=0, sticky=tk.W)

    #w = tk.Spinbox(buttons_frame, from_=0, to=10)
    #w.grid(row=1, column=1, padx=240, sticky=tk.W)

    
    def language(*args):

        def Arabă():
            return 'ar'

        def Chineză():
            return 'zh'
        
        def Ebraică():
            return 'he'
        
        def Engleză():
            return 'en'
        
        def Franceză():
            return 'fr'
        
        def Germană():
            return 'de'
        
        def Italiană():
            return 'it'
        
        def Norvegiană():
            return 'no'
        
        def Olandeză():
            return 'nl'
        
        def Portugheză():
            return 'pt'
        
        def Rusă():
            return 'ru'
        
        def Spaniolă():
            return 'es'
        
        def Suedeză():
            return 'sv'
        
        def Turcă():
            return 'ud'


        switch = {
            'Arabă': Arabă,
            'Chineză': Chineză,
            'Ebraică': Ebraică,
            'Engleză': Engleză,
            'Franceză': Franceză,
            'Germană': Germană,
            'Italiană': Italiană,
            'Norvegiană': Norvegiană,
            'Olandeză': Olandeză,
            'Portugheză': Portugheză,
            'Rusă': Rusă,
            'Spaniolă': Spaniolă,
            'Suedeză': Suedeză,
            'Turcă': Turcă
            }
        case=option.get()
        switch_case = switch.get(case)
        print(f"switch_case este {switch_case}")
        return switch_case()
    option = tk.StringVar(buttons_frame)
    option.set('Engleză')  
    option.trace_add('write', language)
    lang=language()
    print(f"lang este {lang}")

    choices = {'Arabă', 'Chineză', 'Ebraică', 'Engleză', 'Franceză', 'Germană', 'Italiană', 'Norvegiană', 'Olandeză', 'Portugheză', 'Rusă', 'Spaniolă', 'Suedeză', 'Turcă'}
    
    popupMenu = tk.OptionMenu(buttons_frame, option, *choices)
    
    print(f"option.get este {option.get()}")
    L5=tk.Label(buttons_frame, text="Alegeți limba: ")
    L5.grid(row=1, column=1, padx=360, sticky=tk.W)
    popupMenu.grid(row=1, column=1, padx=440, sticky=tk.W)

    button = tk.Button(buttons_frame, text="Căutare", command=lambda: keyword_articles(E1.get(), E2.get(), E3.get(), lang))
    button.grid(row=1, column=1, padx=120, sticky=tk.W)
    print(f"option.get este {option.get()}")

def get_articles(apiKey, language, country, category, pageSize, page, q, sources):
    newsapi_url = 'https://newsapi.org/v2/top-headlines'
    parameters = {
        'apiKey': apiKey,
        'language': language,
        'country': country,
        'category': category,
        'pageSize': pageSize,
        'page': page,
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
        return articles, None, None, None, None
    else:
        status = response.json()['status']
        print(f"Status: {status}")
        code = response.json()['code']
        print(f"Code: {code}")
        message = response.json()['message']
        print(f"Message: {message}")
        return None, error, status, code, message
    
    

def keyword_articles(E1, E2, E3, lang):
    q = E1 if E1 else None
    page = E2 if E2 else None
    pageSize = E3 if E3 else None
    language = lang if lang else None
    articles, error, status, code, message = get_articles(apiKey, language=language, country=None, category=None, sources=None , pageSize=pageSize, page=page, q=q)    
    display_articles_gui(articles, error, status, code, message)




def display_articles_gui(articles, error, status, code, message):

    global previous_window
    global window
    global canvas

    
    if previous_window is not None:
        previous_window.destroy()
        
    
    window = tk.Tk()
    window.title("Articole")
    #window.attributes('-fullscreen', True)
    #window.bind('<Escape>', exit_fullscreen)

    

    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set) 
    frame = tk.Frame(canvas)
    canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    canvas.create_window((0, 0), window=frame, anchor='nw')
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    
    if articles:
        for i, article in enumerate(articles, start=1):
            
            if article['title'] != '[Removed]':    
                article_frame = tk.Frame(frame, padx=10)
                article_frame.grid(row=i, sticky=(tk.W, tk.E))
            

                if article['title'] != None:
                    title_label = tk.Label(article_frame, text=f"#{i} {article['title']}", font=("Verdana", 10))
                    title_label.grid(row=0, sticky=(tk.W))
                else:
                    title_label = tk.Label(article_frame, text=f"#{i} Titlu: Nu am identificat titlul articolului.", font=("Verdana", 10))
                    title_label.grid(row=0, sticky=(tk.W))

                if article['source'] != None:
                    source_label = tk.Label(article_frame, text=f"Sursă: {article['source']['name']}", font=("Arial", 12))
                    source_label.grid(row=1, sticky=(tk.W))
                else:
                    source_label = tk.Label(article_frame, text=f"Sursă: Nu am identificat sursa articolului.", font=("Arial", 12))
                    source_label.grid(row=1, sticky=(tk.W))

                if article['author'] != None:
                    author_label = tk.Label(article_frame, text=f"Autori: {article['author']}", font=("Arial", 12))
                    author_label.grid(row=2, sticky=(tk.W))
                else:
                    author_label = tk.Label(article_frame, text=f"Autori: Nu am identificat autorul/autorii.", font=("Arial", 12))
                    author_label.grid(row=2, sticky=(tk.W))

                if article['description'] != None:
                    description_label = tk.Label(article_frame, text=f"Scurtă descriere: {article['description']}", font=("Arial", 12))
                    description_label.grid(row=3, sticky=(tk.W))
                else:
                    description_label = tk.Label(article_frame, text=f"Scurtă descriere: Nu am identificat descrierea articolului.", font=("Arial", 12))
                    description_label.grid(row=3, sticky=(tk.W))

                if article['publishedAt'] != None:
                    publishedAt_label = tk.Label(article_frame, text=f"Publicat la: {article['publishedAt']}", font=("Arial", 12))
                    publishedAt_label.grid(row=4, sticky=(tk.W))
                else:
                    publishedAt_label = tk.Label(article_frame, text=f"Publicat la: Nu am identificat momentul publicării.", font=("Arial", 12))
                    publishedAt_label.grid(row=4, sticky=(tk.W))

                if article['url'] != None:
                    article_url_label = tk.Label(article_frame, text="Link articol:  ", font=("Arial", 12))
                    article_url_label.grid(row=5, sticky=(tk.W))
                    url_label = tk.Label(article_frame, text=f"{article['url']}", font=("Arial", 12), fg="blue", cursor="hand2")
                    url_label.grid(row=5, padx = 100, sticky=(tk.W))
                    url_label.bind("<Button-1>", lambda event, url=article['url']: open_url(event, url))
                else:
                    url_label = tk.Label(article_frame, text=f"Link articol: Nu am identificat link-ul articolului", font=("Arial", 12))
                    url_label.grid(row=5, sticky=(tk.W))

                if article['urlToImage'] != None:
                    image_link_label = tk.Label(article_frame, text="Link imagine: ", font=("Arial", 12))
                    image_link_label.grid(row=6, sticky=(tk.W))
                    urlToImage_label = tk.Label(article_frame, text=f"{article['urlToImage']}", font=("Arial", 12), fg="blue", cursor="hand2")
                    urlToImage_label.grid(row=6, padx = 100, sticky=(tk.W))
                    urlToImage_label.bind("<Button-1>", lambda event, url=article['urlToImage']: open_url(event, url))
                
                    try:
                        response_urlToImage = requests.get(article['urlToImage'])
                        img_data = response_urlToImage.content
                
                        if response_urlToImage.headers['Content-Type'].startswith('image'):
                            img = Image.open(BytesIO(img_data))
                            img = img.resize((1500, 500))
                            photo = ImageTk.PhotoImage(img)
                            img_label = tk.Label(article_frame, image=photo)
                            img_label.image = photo 
                            img_label.grid(row=7, sticky=(tk.W))
                        else:
                            raise ValueError('URL format not supported.')

                        response_urlToImage.raise_for_status()
                    except (RequestException, ValueError) as a:
                         print(f"Error: {a}")
                    
       
                else:
                    urlToImage_label = tk.Label(article_frame, text=f"Link imagine: Nu am identificat link-ul imaginii articolului", font=("Arial", 12))
                    urlToImage_label.grid(row=6, sticky=(tk.W))

            else:
                continue
           
          

           

        buttons(i+1)

    

    elif error:
        error = tk.Label(window, text=f"Network error: {error}", font=("Arial", 12))
        error.grid(row=1, column=0, sticky=(tk.W))
        status = tk.Label(window, text=f"Status: {status}", font=("Arial", 12))
        status.grid(row=2, column=0, sticky=(tk.W))
        code = tk.Label(window, text=f"Cod: {code}", font=("Arial", 12))
        code.grid(row=3, column=0, sticky=(tk.W))
        message = tk.Label(window, text=f"Mesaj: {message}", font=("Arial", 12))
        message.grid(row=4, column=0, sticky=(tk.W))
        buttons(5)

    else:
        no_articles = tk.Label(window, text="Nu s-au găsit articole. Încercați din nou.", font=("Arial", 12))
        no_articles.grid(row=0, column=0, sticky=(tk.W))
        buttons(1)
    
    window.update()
    canvas.configure(scrollregion=canvas.bbox('all'))

    previous_window = window
    window.mainloop()

if __name__ == "__main__":
    apiKey = '33064a07856d4cf98dd5fd5d759d3ef4'
    articles, error, status, code, message = get_articles(apiKey, language='en' , country=None, category= None, sources=None , pageSize= 3, page = None, q=None)    
    display_articles_gui(articles, error, status, code, message)

    




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