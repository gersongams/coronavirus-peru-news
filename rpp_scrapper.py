from utils import website_fetcher, extract_articles
import requests
from bs4 import BeautifulSoup
import unicodedata


class RPPScrapper():
    diary = "RPP"
    base_url_rpp = "https://rpp.pe"
    url_coronavirus_news = "https://rpp.pe/noticias/coronavirus?ref=rpp"
    soup = []
    articles = []
    articles_soup = []

    def __init__(self, limit=5):
        self.limit = limit

    def fetch_news(self):
        self.soup = website_fetcher(self.url_coronavirus_news)

    def fetch_articles(self):
        articles_soup = self.soup.findAll("article")
        self.articles_soup = articles_soup[:self.limit]

    def get_data_from_articles(self, story):
        time = story.find("time", {"class": "x-ago"})
        title = story.find("h2").find("a")
        subtitle = story.find("p")
        description = unicodedata.normalize("NFKD", subtitle.get_text())

        return {
            "time": time.get("data-x"),
            "title": title.get_text(),
            "img_src": self.get_internal_image(title.get('href')),
            "subtitle": description,
            "article_url": title.get('href')
        }

    def get_internal_image(self, article_url):
        article = requests.get(article_url)
        article_soup = BeautifulSoup(article.content, 'html.parser')

        picture = article_soup.find("div", {"class": "cover"})
        img = picture.find("img")

        return img.get('src')

    def build_json_articles(self):
        self.articles = extract_articles(
            self.articles_soup, self.get_data_from_articles)

    def get_articles(self):
        self.fetch_news()
        self.fetch_articles()
        self.build_json_articles()

        return {
            "diary": self.diary,
            "articles": self.articles
        }
