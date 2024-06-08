import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    return os.getenv('GOOGLE_SEARCH_API_KEY')

def get_search_engine_id():
    return os.getenv('GOOGLE_SEARCH_ENGINE_ID')

import requests

def query_google_search_engine(query='What is quantum entanglement?'):
    api_key = get_api_key()
    id = get_search_engine_id()
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q' : query,
        'key' : api_key,
        'cx' : id
    }
    response = requests.get(url, params)
    results = response.json()

    if 'items' in results:
        links = []
        for item in results['items']:
            item_info = {
                'title': item.get('title', 'No Title'),
                'link': item.get('link', 'No Link'),
                'snippet': item.get('snippet', 'No Snippet')
                }
            links.append(item_info)
        return links
    print(response.text)

if __name__ == "__main__":
    print(query_google_search_engine())