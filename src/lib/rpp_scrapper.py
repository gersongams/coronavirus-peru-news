import json
import unicodedata

from utils import extract_articles, website_fetcher


class RPPScrapper():
    diary = "RPP"
    diary_id = "rpp"
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
        article_url = title.get('href')
        return {
            "time": time.get("data-x"),
            "title": title.get_text(),
            "img_src": self.get_internal_image(article_url),
            "subtitle": description,
            "article_url": article_url
        }

    def get_internal_image(self, article_url):
        article_soup = website_fetcher(article_url)
        img = article_soup.find("meta",  property="og:image")
        img_src = img.get('content')

    def build_json_articles(self):
        self.articles = extract_articles(
            self.articles_soup, self.get_data_from_articles)

    def get_articles(self):
        self.fetch_news()
        self.fetch_articles()
        self.build_json_articles()

        return {
            "diary_id": self.diary_id,
            "diary": self.diary,
            "articles": self.articles
        }
