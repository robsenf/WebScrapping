import requests
import bs4
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen, Request
import csv
import os

# result = requests.get("https://www.goodreads.com/quotes/tag/inspirational?page=0")
# print(result.text)  # or do something with the response

robots = requests.get("https://www.goodreads.com/robots.txt")
robots_result = bs4.BeautifulSoup(robots.text, "lxml")

def download_goodreads_quotes(tag, max_pages=1, max_quotes=50, filename='goodreads_quotes.csv'):
    def download_quotes_from_page(tag, page):
        def compile_url(tag, page):
            return f'https://www.goodreads.com/quotes/tag/motivational'

        def get_soup(url):
            response = urlopen(Request(url))
            return BeautifulSoup(response, 'html.parser')

        def extract_quotes_elements_from_soup(soup):
            elements_quotes = soup.find_all("div", {"class": "quote mediumText"})
            return elements_quotes

        def extract_quote_dict(quote_element):
            def extract_quote(quote_element):
                try:
                    quote = quote_element.find('div', {'class': 'quoteText'}).get_text("|", strip=True)
                    quote = quote.split('|')[0]
                    quote = re.sub('^“', '', quote)
                    quote = re.sub('”\s?$', '', quote)
                    return quote
                except:
                    return None

            def extract_author(quote_element):
                try:
                    author = quote_element.find('span', {'class': 'authorOrTitle'}).get_text()
                    author = author.strip()
                    author = author.rstrip(',')
                    return author
                except:
                    return None

            def extract_source(quote_element):
                try:
                    source = quote_element.find('a', {'class': 'authorOrTitle'}).get_text()
                    return source
                except:
                    return None

            def extract_tags(quote_element):
                try:
                    tags = quote_element.find('div', {'class': 'greyText smallText left'}).get_text(strip=True)
                    tags = re.sub('^tags:', '', tags)
                    tags = tags.split(',')
                    return tags
                except:
                    return None

            def extract_likes(quote_element):
                try:
                    likes = quote_element.find('a', {'class': 'smallText', 'title': 'View this quote'}).get_text(strip=True)
                    likes = re.sub('likes$', '', likes)
                    likes = likes.strip()
                    return int(likes)
                except:
                    return None

            quote_data = {
                'quote': extract_quote(quote_element),
                'author': extract_author(quote_element),
                'source': extract_source(quote_element),
                'likes': extract_likes(quote_element),
                'tags': extract_tags(quote_element)
            }
            return quote_data

        url = compile_url(tag, page)
        print(f'Retrieving {url}...')
        soup = get_soup(url)
        quote_elements = extract_quotes_elements_from_soup(soup)
        return [extract_quote_dict(e) for e in quote_elements]

    def download_all_pages(tag, max_pages, max_quotes):
        results = []
        p = 1
        while p <= max_pages:
            res = download_quotes_from_page(tag, p)
            if len(res) == 0:
                print(f'No results found on page {p}.\nTerminating search.')
                return results

            results = results + res

            if len(results) >= max_quotes:
                print(f'Hit quote maximum ({max_quotes}) on page {p}.\nDiscontinuing search.')
                return results[0:max_quotes]
            else:
                p += 1

        return results

    results = download_all_pages(tag, max_pages, max_quotes)
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['quote', 'author', 'source', 'likes', 'tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for quote in results:
            writer.writerow(quote)
            
    print(f'Successfully saved {len(results)} quotes to {filename}')

# Call the function to download quotes and save to CSV
download_goodreads_quotes('motivational', max_pages=3, max_quotes=50, filename='motivational_quotes.csv')