import datetime
import re

import requests
from bs4 import BeautifulSoup


def website_fetcher(url):
    soup = None
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
    except Exception as ex:
        print(str(ex))
    finally:
        return soup

def extract_articles(articles_soup, extract_function):
    articles = []
    for article in articles_soup:
        try:
            article_json = extract_function(article)
            articles.append(article_json)
        except Exception as ex:
            print(str(ex))
        finally:
            pass

    return articles


def format_time(time):
    month_dict = {
        "Ene": 1,
        "Feb": 2,
        "Mar": 3,
        "Abr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Ago": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dic": 12,
    }

    str = "29 Mar 2020 | 1:48 h"

    date_numbers = re.findall(r'\w+', time)

    year = int(date_numbers[2])
    day = int(date_numbers[0])
    month = month_dict.get(date_numbers[1])
    hour = int(date_numbers[3])
    minute = int(date_numbers[4])

    date = datetime.datetime(year, month, day, hour, minute)
    return date.isoformat()
