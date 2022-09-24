from bs4 import BeautifulSoup
import re
import requests
import numpy as np
import pandas as pd


quote_texts = []
quote_authors = []
quote_tags = []
quote_likes = []

for page in range(1, 101):
    print(f'Downloading page {page}')
    html_text = requests.get(f'https://www.goodreads.com/quotes/tag/science?page={page}').text
    soup = BeautifulSoup(html_text, 'lxml')

    quotes = soup.find_all('div', class_='quote mediumText')

    for quote in quotes:
        quote_details = quote.div
        quote_text_and_author = quote_details.find('div', class_='quoteText').text.replace('\n', '')
        quote_text, quote_author = quote_text_and_author.split(' ― ')
        quote_text = quote_text.strip()[1:-1]
        quote_author = quote_author.strip()
        quote_tag = quote_details.find('div', class_='greyText smallText left').text.replace('\n', '').strip()
        quote_like = quote_details.find('div', class_='quoteFooter').find('div', class_='right').text.strip()

        pattern = r'([\w\d-]+)'
        tags_list = re.findall(pattern, quote_tag)[1:]

        pattern = r'(\d+)'
        likes = int(re.match(pattern, quote_like).groups()[0])

        quote_texts.append(quote_text)
        quote_authors.append(quote_author)
        quote_tags.append(tags_list)
        quote_likes.append(likes)

df = pd.DataFrame({'text': quote_texts, 'author':quote_authors, 'tags':quote_tags, 'likes': quote_likes})
df.to_csv('quotes.csv', index=False)