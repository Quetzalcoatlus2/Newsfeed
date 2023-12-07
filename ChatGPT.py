import requests

def get_news(api_key, country, category, page_size):
    base_url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': api_key,
        'country': country,
        'category': category,
        'pageSize': page_size,
        
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def display_news(news):
    if news:
        for index, article in enumerate(news, start=1):
            print(f"#{index} {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   URL: {article['url']}")
            print("\n")
    else:
        print("No news available.")

if __name__ == "__main__":
    #Sursă cheie API: https://newsapi.org/
    api_key = '33064a07856d4cf98dd5fd5d759d3ef4'
    
    # la 'country' se completează codul țării cu majuscule, minuscule sau ambele: RO, US, GB, AU, NZ, CA, IN, HU, BG, PT, FR, IT, DE, CN etc
    news = get_news(api_key, country='us', category='health', page_size=5)
    
    display_news(news)