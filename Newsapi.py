import requests
from requests.exceptions import RequestException
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser

#spatiere, variabile, culori font, buguri
old_window = None
totalResults = 0

language_codes = {
    'Arabă': 'ar',
    'Chineză': 'zh',
    'Ebraică': 'he',
    'Engleză': 'en',
    'Franceză': 'fr',
    'Germană': 'de',
    'Italiană': 'it',
    'Norvegiană': 'no',
    'Olandeză': 'nl',
    'Portugheză': 'pt',
    'Rusă': 'ru',
    'Spaniolă': 'es',
    'Suedeză': 'sv',
    'Turcă': 'tr'
}

country_codes = {
    'Africa de Sud' : 'za',
    'Arabia Saudită' : 'sa',
    'Argentina' : 'ar',
    'Australia' : 'au',
    'Austria' : 'at',
    'Belgia' : 'be',
    'Brazilia' : 'br',
    'Bulgaria' : 'bg',
    'Canada' : 'ca',
    'Cehia' : 'cz',
    'China' : 'cn',
    'Columbia' : 'co',
    'Coreea de Sud' : 'kr',
    'Cuba' : 'cu',
    'Egipt' : 'eg',
    'Elveția' : 'ch',
    'Emiratele Arabe Unite' : 'ae',
    'Filipine' : 'ph',
    'Franța' : 'fr',
    'Germania' : 'de',
    'Grecia' : 'gr',
    'Hong Kong' : 'hk',
    'India' : 'in',
    'Indonezia' : 'id',
    'Irlanda' : 'ie',
    'Israel' : 'il',
    'Italia' : 'it',
    'Japonia' : 'jp',
    'Letonia' : 'lv',
    'Lituania' : 'lt',
    'Malaezia' : 'my',
    'Marea Britanie' : 'gb',
    'Maroc' : 'ma',
    'Mexic' : 'mx',
    'Nigeria' : 'ng',
    'Norvegia' : 'no',
    'Noua Zeelandă' : 'nz',
    'Olanda' : 'nl',
    'Polonia' : 'pl',
    'Portugalia' : 'pt',
    'România' : 'ro',
    'Rusia' : 'ru',
    'Serbia' : 'rs',
    'Singapore' : 'sg',
    'Slovacia' : 'sk',
    'Slovenia' : 'si',
    'Statele Unite ale Americii' : 'us',
    'Suedia' : 'se',
    'Taiwan' : 'tw',
    'Thailanda' : 'th',
    'Turcia' : 'tr',
    'Ucraina' : 'ua',
    'Ungaria' : 'hu',
    'Venezuela' : 've'
}

category_codes = {
    'Afaceri': 'business',
    'Divertisment': 'entertainment',
    'General': 'general',
    'Sănătate': 'health',
    'Sport': 'sport',
    'Știință': 'science',
    'Tehnologie': 'technology'
}

sources_codes = {
    'Google News' : 'google-news', 
    'BBC News' : 'bbc-news',
    'The Verge': 'the-verge', 
    'CNN' : 'cnn', 
    'USA Today' : 'usa-today', 
    'ABC News' : 'abc-news', 
    'Associated Press' : 'associated-press', 
    'Axios' : 'axios', 
    'Bloomberg' : 'bloomberg', 
    'Bussiness Insider' : 'business-insider', 
    'CBC News' : 'cbc-news', 
    'CNBC' : 'cnbc', 
    'Engadget' : 'engadget', 
    'Entertainment Weekly' : 'entertainment-weekly', 
    'Fortune' : 'fortune', 
    'For Sports' : 'fox-sports', 
    'Google News California' : 'google-news-ca', 
    'Google News Marea Britanie' : 'google-news-uk', 
    'Hacker News' : 'hacker-news', 
    'IGN' : 'ign', 
    'Medical News Today' : 'medical-news-today', 
    'MSNBC' : 'msnbc', 
    'MTV News' : 'mtv-news', 
    'National Geographic' : 'national-geographic', 
    'NBC News' : 'nbc-news', 
    'News24' : 'news24', 
    'Newsweek' : 'newsweek', 
    'New York Magazine' : 'new-york-magazine', 
    'Next Big Future' : 'next-big-future', 
    'NFL News' : 'nfl-news', 
    'NHL News' : 'nhl-news', 
    'Politico' : 'politico', 
    'Polygon' : 'polygon', 
    'Recode' : 'recode', 
    'Reddit r/all' : 'reddit-r-all', 
    'Reuters' : 'reuters', 
    'Techcrunch' : 'techcrunch', 
    'Techradar' : 'techradar', 
    'The American Conservative' : 'the-american-conservative', 
    'The Hill' : 'the-hill', 
    'The Huffington Post' : 'the-huffington-post', 
    'The Next Web' : 'the-next-web', 
    'The Sport Bible' : 'the-sport-bible', 
    'The Times of India' : 'the-times-of-india', 
    'The Washignton Post' : 'the-washington-times', 
    'Time' : 'time', 
    'Vice News' : 'vice-news', 
    'Wired' : 'wired'
}



def call_articles(apiKey, language, country, category, pageSize, page, q, sources):
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




def articles_gui(articles, error, status, code, message):

    global old_window
    global window
    global canvas

    
    def scroll(action):
        canvas.yview_scroll(int(-1*(action.delta/80)), "u")

    if old_window is not None:
        old_window.destroy()
        
    
    window = tk.Tk()
    window.title("Newsfeed")
    #window.attributes('-fullscreen', True)
    #window.bind('<Escape>', exit_fullscreen)


    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient = 'vertical', command = canvas.yview)
    canvas.configure(yscrollcommand = scrollbar.set) 
    frame = tk.Frame(canvas)
    canvas.grid(row = 0, column = 0, sticky = (tk.N, tk.S, tk.E, tk.W))
    scrollbar.grid(row = 0, column = 1, sticky = (tk.N, tk.S))
    canvas.create_window((0, 0), window = frame, anchor = 'nw')
    canvas.bind_all("<MouseWheel>", scroll)
    window.grid_rowconfigure(0, weight = 1)
    window.grid_columnconfigure(0, weight = 1)

    
    if articles:
        for i, article in enumerate(articles, start = 1):
            
            if article['title'] != '[Removed]':    

                article_frame = tk.Frame(frame, padx = 10, pady = 10, bd = 5, relief = tk.RIDGE)
                article_frame.grid(row = i, sticky = (tk.W, tk.E))
            

                if article['title'] != None:
                    title_label = tk.Label(article_frame, text = f"#{i} {article['title']}", font = ("System", 16))
                    title_label.grid(row = 0, sticky = (tk.W))
                else:
                    title_label = tk.Label(article_frame, text = f"#{i} Titlu: Nu am identificat titlul articolului.", font = ("System", 16))
                    title_label.grid(row = 0, sticky = (tk.W))

                if article['description'] != None:
                    description_label = tk.Label(article_frame, text = f"Scurtă descriere: {article['description']}", font = ("Verdana", 8))
                    description_label.grid(row = 1, sticky = (tk.W))
                else:
                    description_label = tk.Label(article_frame, text = f"Scurtă descriere: Nu am identificat descrierea articolului.", font = ("Verdana", 8))
                    description_label.grid(row = 1, sticky = (tk.W))

                if article['source'] != None:
                    source_label = tk.Label(article_frame, text = f"Sursă: {article['source']['name']}", font = ("Verdana", 8))
                    source_label.grid(row = 2, sticky = (tk.W))
                else:
                    source_label = tk.Label(article_frame, text = f"Sursă: Nu am identificat sursa articolului.", font = ("Verdana", 8))
                    source_label.grid(row = 2, sticky = (tk.W))

                if article['author'] != None:
                    author_label = tk.Label(article_frame, text = f"Autori: {article['author']}", font = ("Verdana", 8))
                    author_label.grid(row = 3, sticky = (tk.W))
                else:
                    author_label = tk.Label(article_frame, text = f"Autori: Nu am identificat autorul/autorii.", font = ("Verdana", 8))
                    author_label.grid(row = 3, sticky = (tk.W))

                if article['publishedAt'] != None:
                    publishedAt_label = tk.Label(article_frame, text = f"Publicat la: {article['publishedAt']}", font = ("Verdana", 8))
                    publishedAt_label.grid(row = 4, sticky = (tk.W))
                else:
                    publishedAt_label = tk.Label(article_frame, text = f"Publicat la: Nu am identificat momentul publicării.", font = ("Verdana", 8))
                    publishedAt_label.grid(row = 4, sticky = (tk.W))

                if article['url'] != None:
                    article_url_label = tk.Label(article_frame, text = "Link articol:  ", font = ("Verdana", 5))
                    article_url_label.grid(row = 5, sticky = (tk.W))
                    url_label = tk.Label(article_frame, text = f"{article['url']}", font=("Terminal", 5), fg = "blue", cursor = "hand2")
                    url_label.grid(row = 5, padx = 48, sticky = (tk.W))
                    url_label.bind("<Button-1>", lambda action, url = article['url']: webbrowser.open(url))
                else:
                    url_label = tk.Label(article_frame, text = f"Link articol: Nu am identificat link-ul articolului", font = ("Verdana",6))
                    url_label.grid(row = 5, sticky = (tk.W))

                if article['urlToImage'] != None:
                    image_url_label = tk.Label(article_frame, text = "Link imagine: ", font = ("Verdana", 5))
                    image_url_label.grid(row = 6, sticky = (tk.W))
                    urlToImage_label = tk.Label(article_frame, text = f"{article['urlToImage']}", font = ("Terminal", 5), fg = "blue", cursor = "hand2")
                    urlToImage_label.grid(row = 6, padx = 48, sticky = (tk.W))
                    urlToImage_label.bind("<Button-1>", lambda action, url = article['urlToImage']: webbrowser.open(url))
                
                    try:
                        urlToImage_response = requests.get(article['urlToImage'])
                        urlToImage_content = urlToImage_response.content
                
                        if urlToImage_response.headers['Content-Type'].startswith('image'):
                            urlToImage_image = Image.open(BytesIO(urlToImage_content))
                            urlToImage_resized_image = urlToImage_image.resize((1500, 500))
                            urlToImage_photo = ImageTk.PhotoImage(urlToImage_resized_image)
                            urlToImage_resized_image_label = tk.Label(article_frame, image = urlToImage_photo)
                            urlToImage_resized_image_label.image = urlToImage_photo 
                            urlToImage_resized_image_label.grid(row = 7, sticky = (tk.W))
                        else:
                            raise ValueError('URL format not supported.')

                        urlToImage_response.raise_for_status()

                    except (RequestException, ValueError) as image_error:
                        print(f"Error: {image_error}")
                    
       
                else:
                    urlToImage_label = tk.Label(article_frame, text = f"Link imagine: Nu am identificat link-ul imaginii articolului.", font = ("Verdana", 5))
                    urlToImage_label.grid(row = 6, sticky = (tk.W))


               

            else:
                continue
           
          

        
        buttons(i + 1)

    elif error:

        error = tk.Label(window, text = f"Network error: {error}", font = ("Segoe UI", 11))
        error.grid(row = 1, column = 0, sticky = (tk.W))
        status = tk.Label(window, text = f"Status: {status}", font = ("Segoe UI", 11))
        status.grid(row = 2, column = 0, sticky = (tk.W))
        code = tk.Label(window, text = f"Cod: {code}", font = ("Segoe UI", 11))
        code.grid(row = 3, column = 0, sticky = (tk.W))
        message = tk.Label(window, text = f"Mesaj: {message}", font = ("Segoe UI", 11))
        message.grid(row = 4, column = 0, sticky = (tk.W))
        buttons(5)

    else:

        no_articles = tk.Label(window, text = "Nu s-au găsit articole. Încercați din nou.", font = ("Segoe UI", 60))
        no_articles.grid(row = 0, column = 0, sticky = (tk.W))
        buttons(1)
    

    window.update()
    canvas.configure(scrollregion = canvas.bbox('all'))

    old_window = window
    window.mainloop()


def buttons(i):

    global totalResults

    def language_option_changed(*args):
        language_option.get()

    def country_option_changed(*args):
        country_option.get()

    def category_option_changed(*args):
        category_option.get()

    def sources_option_changed(*args):
        sources_option.get()


    buttons_frame = tk.Frame(window, padx = 10)
    buttons_frame.grid(row = i, sticky = (tk.W, tk.E))

    keyword_label = tk.Label(buttons_frame, text = 'Cuvânt cheie:')
    keyword_label.grid(row = 0, sticky = tk.W)
    keyword_entry = tk.Entry(buttons_frame, bd = 10)
    keyword_entry.grid(row = 0, padx = 80, sticky = tk.W)

    results_per_page_label = tk.Label(buttons_frame, text = 'Articole per pagină:')
    results_per_page_label.grid(row = 0, padx = 250, sticky = tk.W)
    results_per_page_default = tk.IntVar(value = 3)
    results_per_page_spinbox = tk.Spinbox(buttons_frame, from_ = 1, to = 100, textvariable = results_per_page_default)
    results_per_page_spinbox.grid(row = 0, padx = 360, sticky = tk.W)

    page_number_label = tk.Label(buttons_frame, text = 'Numărul paginii:')
    page_number_label.grid(row = 0, padx = 530, sticky = tk.W)
    page_number_spinbox = tk.Spinbox(buttons_frame, from_ = 1, to = 1 + int(totalResults)//int(results_per_page_spinbox.get()))
    page_number_spinbox .grid(row = 0, padx = 630, sticky = tk.W)



    
    """def language(*args):

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
        return switch_case()"""
    

    language_label = tk.Label(buttons_frame, text = "Alegeți limba: ")
    language_label.grid(row = 1, sticky = tk.W)
    language_option = tk.StringVar(buttons_frame)
    language_option.set(language_option.get())  
    language_choices = {'Arabă', 'Chineză', 'Ebraică', 'Engleză', 'Franceză', 'Germană', 'Italiană', 'Norvegiană', 'Olandeză', 
                        'Portugheză', 'Rusă', 'Spaniolă', 'Suedeză', 'Turcă'}
    language_popupMenu = tk.OptionMenu(buttons_frame, language_option, *language_choices)
    language_popupMenu.grid(row = 1, padx = 80, sticky = tk.W)
    language_option.trace_add('write', language_option_changed)


    country_label = tk.Label(buttons_frame, text = "Alegeți țara: ")
    country_label.grid(row = 1, padx = 250, sticky = tk.W)
    country_option = tk.StringVar(buttons_frame)
    country_option.set(country_option.get())  
    country_choices = {'Africa de Sud', 'Arabia Saudită', 'Argentina', 'Australia' , 'Austria', 'Belgia', 'Brazilia', 'Bulgaria', 
                       'Canada', 'Cehia', 'China', 'Columbia', 'Coreea de Sud', 'Cuba', 'Egipt', 'Elveția', 'Emiratele Arabe Unite', 
                       'Filipine', 'Franța', 'Germania', 'Grecia', 'Hong Kong', 'India', 'Indonezia', 'Irlanda', 'Israel', 'Italia', 
                       'Japonia', 'Letonia', 'Lituania', 'Malaezia', 'Marea Britanie', 'Maroc', 'Mexic', 'Nigeria', 'Norvegia', 
                       'Noua Zeelandă', 'Olanda', 'Polonia', 'Portugalia', 'România', 'Rusia', 'Serbia', 'Singapore', 'Slovacia', 
                       'Slovenia', 'Statele Unite ale Americii', 'Suedia', 'Taiwan', 'Thailanda', 'Turcia', 'Ucraina', 'Ungaria', 
                       'Venezuela'}
    country_popupMenu = tk.OptionMenu(buttons_frame, country_option, *country_choices)
    country_popupMenu.grid(row = 1, padx = 320, sticky = tk.W)
    country_option.trace_add('write', country_option_changed)

    category_label = tk.Label(buttons_frame, text = "Alegeți categoria: ")
    category_label.grid(row = 1, padx = 530, sticky = tk.W)
    category_option = tk.StringVar(buttons_frame)
    category_option.set(category_option.get())  
    category_choices = {'Afaceri', 'Divertisment', 'General', 'Sănătate', 'Sport', 'Știință', 'Tehnologie'}
    category_popupMenu = tk.OptionMenu(buttons_frame, category_option, *category_choices)
    category_popupMenu.grid(row = 1, padx = 630, sticky = tk.W)
    category_option.trace_add('write', category_option_changed)

    source_label = tk.Label(buttons_frame, text = "Alegeți sursa: ")
    source_label.grid(row = 1, padx = 800, sticky = tk.W)
    sources_option = tk.StringVar(buttons_frame)
    sources_option.set(sources_option.get())  
    sources_choices = {'Google News', 'BBC News', 'The Verge', 'CNN', 'USA Today', 'ABC News', 'Associated Press', 'Axios', 'Bloomberg',
                       'Bussiness Insider', 'CBC News', 'CNBC', 'Engadget', 'Entertainment Weekly', 'Fortune', 'For Sports',
                       'Google News California', 'Google News Marea Britanie', 'Hacker News', 'IGN', 'Medical News Today', 'MSNBC', 
                       'MTV News', 'National Geographic', 'NBC News', 'News24', 'Newsweek', 'New York Magazine', 'Next Big Future', 
                       'NFL News', 'NHL News', 'Politico', 'Polygon', 'Recode', 'Reddit r/all', 'Reuters', 'Techcrunch', 'Techradar', 
                       'The American Conservative', 'The Hill', 'The Huffington Post', 'The Next Web', 'The Sport Bible', 
                       'The Times of India', 'The Washignton Post', 'Time', 'Vice News', 'Wired'}
    sources_popupMenu = tk.OptionMenu(buttons_frame, sources_option, *sources_choices)
    sources_popupMenu.grid(row = 1, padx = 880, sticky = tk.W)
    sources_option.trace_add('write', sources_option_changed)


    totalResults_label = tk.Label(buttons_frame, text = f"Număr rezultate: {totalResults}")
    totalResults_label.grid(row = 0, padx = 1390, sticky = tk.W)


    button = tk.Button(buttons_frame, text = "Apăsați acest buton după ce ați ales toți parametrii pentru căutare.", 
                       command = lambda: articles_search(keyword_entry.get(), results_per_page_spinbox.get(), page_number_spinbox.get(), language_option.get(), country_option.get(), category_option.get(), sources_option.get()))
    button.grid(row = 1, padx = 1145, sticky = tk.W)




def articles_search(keyword_entry, page_number_spinbox, results_per_page_spinbox , language_option, country_option, category_option, sources_option):

    q = keyword_entry if keyword_entry else None
    pageSize = page_number_spinbox if page_number_spinbox else None
    page = results_per_page_spinbox if results_per_page_spinbox else None
    language = language_codes.get(language_option) if language_option else 'en'
    country = country_codes.get(country_option) if country_option else None
    category = category_codes.get(category_option) if category_option else None
    sources = sources_codes.get(sources_option) if sources_option else None
    sources = {sources} if sources is not None else {}

    articles, error, status, code, message = call_articles(apiKey, language = language, country = country, category = category, sources = sources, pageSize = pageSize, page = page, q = q)    
    articles_gui(articles, error, status, code, message)



if __name__ == "__main__":

    apiKey = '33064a07856d4cf98dd5fd5d759d3ef4'

    articles, error, status, code, message = call_articles(apiKey, language = 'en' , country = None, category = None, sources = None , pageSize = 3, page = None, q=None)    
    articles_gui(articles, error, status, code, message)

    

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



  