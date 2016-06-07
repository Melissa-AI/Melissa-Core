import requests
from bs4 import BeautifulSoup

from SenseCells.tts import tts

# NDTV News
fixed_url = 'http://profit.ndtv.com/news/latest/'
news_headlines_list = []
news_details_list = []

for i in range(1, 2):
    changing_slug = '/page-' + str(i)
    url = fixed_url + changing_slug

    try:
        r  = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")

        for news_headlines in soup.find_all('h2'):
            news_headlines_list.append(news_headlines.get_text())

        del news_headlines_list[-2:]

        for news_details in soup.find_all('p', 'intro'):
            news_details_list.append(news_details.get_text())

        news_headlines_list_small = [element.lower().replace("(", "").replace(")", "").replace("'", "") for element in news_headlines_list]
        news_details_list_small = [element.lower().replace("(", "").replace(")", "").replace("'", "") for element in news_details_list]

        news_dictionary = dict(zip(news_headlines_list_small, news_details_list_small))

    except requests.exceptions.ConnectionError:
        print('You are not connected to the internet, this will limit my capabilities.')

def news_reader():
    for key, value in news_dictionary.items():
        tts('Headline, ' + key)
        tts('News, ' + value)
