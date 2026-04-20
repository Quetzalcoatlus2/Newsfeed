from newsapi import NewsApiClient
import requests
from requests.exceptions import RequestException
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
import math

old_window = None
totalResults = 0

apiKey = NewsApiClient(api_key= '33064a07856d4cf98dd5fd5d759d3ef4')

language_codes = {
    'Arabic': 'ar',
    'Chinese': 'zh',
    'Hebrew': 'he',
    'English': 'en',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Norwegian': 'no',
    'Dutch': 'nl',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Spanish': 'es',
    'Swedish': 'sv',
    'Turkish': 'tr'
}

country_codes = {
    'South Africa' : 'za',
    'Saudi Arabia' : 'sa',
    'Argentina' : 'ar',
    'Australia' : 'au',
    'Austria' : 'at',
    'Belgium' : 'be',
    'Brazil' : 'br',
    'Bulgaria' : 'bg',
    'Canada' : 'ca',
    'Czech Republic' : 'cz',
    'China' : 'cn',
    'Columbia' : 'co',
    'South Korea' : 'kr',
    'Cuba' : 'cu',
    'Egypt' : 'eg',
    'Switzerland' : 'ch',
    'United Arab Emirates' : 'ae',
    'Philippines' : 'ph',
    'France' : 'fr',
    'Germany' : 'de',
    'Greece' : 'gr',
    'Hong Kong' : 'hk',
    'India' : 'in',
    'Indonesia' : 'id',
    'Ireland' : 'ie',
    'Israel' : 'il',
    'Italy' : 'it',
    'Japan' : 'jp',
    'Latvia' : 'lv',
    'Lithuania' : 'lt',
    'Malaysia' : 'my',
    'United Kingdom' : 'gb',
    'Morocco' : 'ma',
    'Mexico' : 'mx',
    'Nigeria' : 'ng',
    'Norway' : 'no',
    'New Zealand' : 'nz',
    'Netherlands' : 'nl',
    'Poland' : 'pl',
    'Portugal' : 'pt',
    'Romania' : 'ro',
    'Russia' : 'ru',
    'Serbia' : 'rs',
    'Singapore' : 'sg',
    'Slovakia' : 'sk',
    'Slovenia' : 'si',
    'United States of America' : 'us',
    'Sweden' : 'se',
    'Taiwan' : 'tw',
    'Thailand' : 'th',
    'Turkey' : 'tr',
    'Ukraine' : 'ua',
    'Hungary' : 'hu',
    'Venezuela' : 've'
}

category_codes = {
    'Business': 'business',
    'Entertainment': 'entertainment',
    'General': 'general',
    'Health': 'health',
    'Sport': 'sport',
    'Science': 'science',
    'Technology': 'technology'
}

sources_codes = {
    'ABC News' : 'abc-news', 
    'Associated Press' : 'associated-press', 
    'Axios' : 'axios', 
    'BBC News' : 'bbc-news',
    'Bloomberg' : 'bloomberg', 
    'Bussiness Insider' : 'business-insider', 
    'CBC News' : 'cbc-news', 
    'CNBC' : 'cnbc', 
    'CNN' : 'cnn', 
    'Engadget' : 'engadget', 
    'Entertainment Weekly' : 'entertainment-weekly', 
    'Fortune' : 'fortune', 
    'For Sports' : 'fox-sports', 
    'Google News' : 'google-news', 
    'Google News California' : 'google-news-ca', 
    'Google News UK' : 'google-news-uk', 
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
    'The Verge': 'the-verge', 
    'The Washignton Post' : 'the-washington-times', 
    'Time' : 'time', 
    'USA Today' : 'usa-today', 
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
            if i == 1:
                totalResults_frame = tk.Frame(frame, padx = 10, pady = 10, bd = 5, relief = tk.RIDGE)
                totalResults_frame.grid(row = 0, sticky = (tk.W, tk.E))
                totalResults_label = tk.Label(totalResults_frame, text = f"Number of results: {totalResults}", font = ("Segoe UI", 20))
                totalResults_label.grid(row = 0, sticky = tk.W)
            
            if article['title'] != '[Removed]':    

                article_frame = tk.Frame(frame, padx = 10, pady = 10, bd = 5, relief = tk.RIDGE)
                article_frame.grid(row = i, sticky = (tk.W, tk.E))

                if article['title'] != None:
                    title_label = tk.Label(article_frame, text = f"#{i} {article['title']}", font = ("System", 16))
                    title_label.grid(row = 1, sticky = (tk.W))
                else:
                    title_label = tk.Label(article_frame, text = f"#{i} Title: The article title could not be identified.", font = ("System", 16))
                    title_label.grid(row = 1, sticky = (tk.W))

                if article['description'] != None:
                    description_label = tk.Label(article_frame, text = f"Short description: {article['description']}", font = ("Verdana", 8))
                    description_label.grid(row = 2, sticky = (tk.W))
                else:
                    description_label = tk.Label(article_frame, text = f"Short description: The article description could not be identified.", font = ("Verdana", 8))
                    description_label.grid(row = 3, sticky = (tk.W))

                if article['source'] != None:
                    source_label = tk.Label(article_frame, text = f"Source: {article['source']['name']}", font = ("Verdana", 8))
                    source_label.grid(row = 3, sticky = (tk.W))
                else:
                    source_label = tk.Label(article_frame, text = f"Source: The article source could not be identified.", font = ("Verdana", 8))
                    source_label.grid(row = 3, sticky = (tk.W))

                if article['author'] != None:
                    author_label = tk.Label(article_frame, text = f"Authors: {article['author']}", font = ("Verdana", 8))
                    author_label.grid(row = 4, sticky = (tk.W))
                else:
                    author_label = tk.Label(article_frame, text = f"Authors: The author(s) could not be identified.", font = ("Verdana", 8))
                    author_label.grid(row = 4, sticky = (tk.W))

                if article['publishedAt'] != None:
                    publishedAt_label = tk.Label(article_frame, text = f"Published at: {article['publishedAt']}", font = ("Verdana", 8))
                    publishedAt_label.grid(row = 5, sticky = (tk.W))
                else:
                    publishedAt_label = tk.Label(article_frame, text = f"Published at: The publication time could not be identified.", font = ("Verdana", 8))
                    publishedAt_label.grid(row = 5, sticky = (tk.W))

                if article['url'] != None:
                    article_url_label = tk.Label(article_frame, text = "Article link:  ", font = ("Verdana", 5))
                    article_url_label.grid(row = 6, sticky = (tk.W))
                    url_label = tk.Label(article_frame, text = f"{article['url']}", font=("Terminal", 5), fg = "blue", cursor = "hand2")
                    url_label.grid(row = 6, padx = 48, sticky = (tk.W))
                    url_label.bind("<Button-1>", lambda action, url = article['url']: webbrowser.open(url))
                else:
                    url_label = tk.Label(article_frame, text = f"Article link: The article link could not be identified.", font = ("Verdana",6))
                    url_label.grid(row = 6, sticky = (tk.W))

                if article['urlToImage'] != None:
                    image_url_label = tk.Label(article_frame, text = "Image link: ", font = ("Verdana", 5))
                    image_url_label.grid(row = 7, sticky = (tk.W))
                    urlToImage_label = tk.Label(article_frame, text = f"{article['urlToImage']}", font = ("Terminal", 5), fg = "blue", cursor = "hand2")
                    urlToImage_label.grid(row = 7, padx = 48, sticky = (tk.W))
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
                            urlToImage_resized_image_label.grid(row = 8, sticky = (tk.W))
                        else:
                            raise ValueError('URL format not supported.')

                        urlToImage_response.raise_for_status()

                    except (RequestException, ValueError) as image_error:
                        print(f"Error: {image_error}")
                    
       
                else:
                    urlToImage_label = tk.Label(article_frame, text = f"Image link: The article image link could not be identified.", font = ("Verdana", 5))
                    urlToImage_label.grid(row = 7, sticky = (tk.W))


               

            else:
                continue
           
          

        
        buttons(i + 1)

    elif error:
        error_label = tk.Label(window, text = f"Network error: {error}", font = ("Segoe UI", 11))
        error_label .grid(row = 1, column = 0, sticky = (tk.W))
        status_label  = tk.Label(window, text = f"Status: {status}", font = ("Segoe UI", 11))
        status_label .grid(row = 2, column = 0, sticky = (tk.W))
        code_label  = tk.Label(window, text = f"Code: {code}", font = ("Segoe UI", 11))
        code_label .grid(row = 3, column = 0, sticky = (tk.W))
        message_label  = tk.Label(window, text = f"Message: {message}", font = ("Segoe UI", 11))
        message_label .grid(row = 4, column = 0, sticky = (tk.W))
        buttons(5)

    else:
        no_articles = tk.Label(window, text = "No articles were found. Please try again.", font = ("Segoe UI", 60))
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

    keyword_label = tk.Label(buttons_frame, text = 'Keyword:')
    keyword_label.grid(row = 0, sticky = tk.W)
    keyword_entry = tk.Entry(buttons_frame, bd = 10)
    keyword_entry.grid(row = 0, padx = 80, sticky = tk.W)

    results_per_page_label = tk.Label(buttons_frame, text = 'Articles per page:')
    results_per_page_label.grid(row = 0, padx = 250, sticky = tk.W)
    results_per_page_default = tk.IntVar(value = 3)
    results_per_page_spinbox = tk.Spinbox(buttons_frame, from_ = 1, to = 100, textvariable = results_per_page_default)
    results_per_page_spinbox.grid(row = 0, padx = 360, sticky = tk.W)

    page_number_label = tk.Label(buttons_frame, text = 'Page number:')
    page_number_label.grid(row = 0, padx = 530, sticky = tk.W)
    page_number_spinbox = tk.Spinbox(buttons_frame, from_ = 1, to = math.ceil(totalResults / int(results_per_page_spinbox.get())) if totalResults else 1)
    page_number_spinbox .grid(row = 0, padx = 630, sticky = tk.W)



    
    """def language(*args):

        def Arabic():
            return 'ar'

        def Chinese():
            return 'zh'
        
        def Hebrew():
            return 'he'
        
        def English():
            return 'en'
        
        def French():
            return 'fr'
        
        def German():
            return 'de'
        
        def Italian():
            return 'it'
        
        def Norwegian():
            return 'no'
        
        def Dutch():
            return 'nl'
        
        def Portuguese():
            return 'pt'
        
        def Russian():
            return 'ru'
        
        def Spanish():
            return 'es'
        
        def Swedish():
            return 'sv'
        
        def Turkish():
            return 'tr'


        switch = {
            'Arabic': Arabic,
            'Chinese': Chinese,
            'Hebrew': Hebrew,
            'English': English,
            'French': French,
            'German': German,
            'Italian': Italian,
            'Norwegian': Norwegian,
            'Dutch': Dutch,
            'Portuguese': Portuguese,
            'Russian': Russian,
            'Spanish': Spanish,
            'Swedish': Swedish,
            'Turkish': Turkish
            }
        case=option.get()
        switch_case = switch.get(case)
        print(f"switch_case is {switch_case}")
        return switch_case()"""
    

    language_label = tk.Label(buttons_frame, text = "Choose language: ")
    language_label.grid(row = 1, sticky = tk.W)
    language_option = tk.StringVar(buttons_frame)
    language_option.set(language_option.get())  
    language_choices = {'Arabic', 'Chinese', 'Hebrew', 'English', 'French', 'German', 'Italian', 'Norwegian', 'Dutch', 
                        'Portuguese', 'Russian', 'Spanish', 'Swedish', 'Turkish'}
    language_popupMenu = tk.OptionMenu(buttons_frame, language_option, *language_choices)
    language_popupMenu.grid(row = 1, padx = 80, sticky = tk.W)
    language_option.trace_add('write', language_option_changed)


    country_label = tk.Label(buttons_frame, text = "Choose country: ")
    country_label.grid(row = 1, padx = 250, sticky = tk.W)
    country_option = tk.StringVar(buttons_frame)
    country_option.set(country_option.get())  
    country_choices = {'South Africa', 'Saudi Arabia', 'Argentina', 'Australia' , 'Austria', 'Belgium', 'Brazil', 'Bulgaria', 
                       'Canada', 'Czech Republic', 'China', 'Columbia', 'South Korea', 'Cuba', 'Egypt', 'Switzerland', 'United Arab Emirates', 
                       'Philippines', 'France', 'Germany', 'Greece', 'Hong Kong', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 
                       'Japan', 'Latvia', 'Lithuania', 'Malaysia', 'United Kingdom', 'Morocco', 'Mexico', 'Nigeria', 'Norway', 
                       'New Zealand', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Russia', 'Serbia', 'Singapore', 'Slovakia', 
                       'Slovenia', 'United States of America', 'Sweden', 'Taiwan', 'Thailand', 'Turkey', 'Ukraine', 'Hungary', 
                       'Venezuela'}
    country_popupMenu = tk.OptionMenu(buttons_frame, country_option, *country_choices)
    country_popupMenu.grid(row = 1, padx = 320, sticky = tk.W)
    country_option.trace_add('write', country_option_changed)

    category_label = tk.Label(buttons_frame, text = "Choose category: ")
    category_label.grid(row = 1, padx = 530, sticky = tk.W)
    category_option = tk.StringVar(buttons_frame)
    category_option.set(category_option.get())  
    category_choices = {'Business', 'Entertainment', 'General', 'Health', 'Sport', 'Science', 'Technology'}
    category_popupMenu = tk.OptionMenu(buttons_frame, category_option, *category_choices)
    category_popupMenu.grid(row = 1, padx = 630, sticky = tk.W)
    category_option.trace_add('write', category_option_changed)

    source_label = tk.Label(buttons_frame, text = "Choose source: ")
    source_label.grid(row = 1, padx = 767, sticky = tk.W)
    sources_option = tk.StringVar(buttons_frame)
    sources_option.set(sources_option.get())  
    sources_choices = {'Google News', 'BBC News', 'The Verge', 'CNN', 'USA Today', 'ABC News', 'Associated Press', 'Axios', 'Bloomberg',
                       'Bussiness Insider', 'CBC News', 'CNBC', 'Engadget', 'Entertainment Weekly', 'Fortune', 'For Sports',
                       'Google News California', 'Google News UK', 'Hacker News', 'IGN', 'Medical News Today', 'MSNBC', 
                       'MTV News', 'National Geographic', 'NBC News', 'News24', 'Newsweek', 'New York Magazine', 'Next Big Future', 
                       'NFL News', 'NHL News', 'Politico', 'Polygon', 'Recode', 'Reddit r/all', 'Reuters', 'Techcrunch', 'Techradar', 
                       'The American Conservative', 'The Hill', 'The Huffington Post', 'The Next Web', 'The Sport Bible', 
                       'The Times of India', 'The Washignton Post', 'Time', 'Vice News', 'Wired'}
    sources_popupMenu = tk.OptionMenu(buttons_frame, sources_option, *sources_choices)
    sources_popupMenu.grid(row = 1, padx = 840, sticky = tk.W)
    sources_option.trace_add('write', sources_option_changed)




    button = tk.Button(buttons_frame, text = "CLICK THIS BUTTON AFTER YOU HAVE CHOSEN ALL THE SEARCH PARAMETERS YOU WANT!", 
                       command = lambda: articles_search(keyword_entry.get(), results_per_page_spinbox.get(), page_number_spinbox.get(), 
                       language_option.get(), country_option.get(), category_option.get(), sources_option.get()))
    button.grid(row = 1, padx = 1035, sticky = tk.W)



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
