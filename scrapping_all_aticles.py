import requests
import bs4
from fake_useragent import UserAgent
import re


KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'linux']
url = 'https://habr.com/ru'

response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')

for article in articles:
    href = article.find(class_="tm-article-snippet__title-link").attrs['href']
    link = url + href[3:]
    resp = requests.get(link, headers={'User-Agent': UserAgent().chrome})
    article_text = resp.text

    soup = bs4.BeautifulSoup(article_text, features='html.parser')
    article_t = soup.find_all('p')
    for word in KEYWORDS:
        if re.search(rf'\b{word}\b', str(article_t).lower()):
            dt = article.find(class_='tm-article-snippet__datetime-published').time.attrs['title']
            title = article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").text
            print(f'{dt} - {title} - {link}')
            break
