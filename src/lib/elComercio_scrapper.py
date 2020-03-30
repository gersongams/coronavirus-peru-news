import unicodedata

from utils import extract_articles, website_fetcher


class ElComercioScrapper():
    diary = "El Comercio"
    diary_id = "el_comercio"
    base_url_elComercio = "https://elcomercio.pe"
    url_coronavirus_news = "https://elcomercio.pe/noticias/coronavirus-peru/"
    soup = []
    articles = []
    articles_soup = []

    def __init__(self, limit=5):
        self.limit = limit

    def fetch_news(self):
        self.soup = website_fetcher(self.url_coronavirus_news)

    def fetch_articles(self):
        articles_soup = self.soup.findAll("div", {"class": "story-item"})
        self.articles_soup = articles_soup[:self.limit]

    def get_data_from_articles(self, story):
        title = story.find("a", {"class": "story-item__title"})
        subtitle = story.find("p", {"class": "story-item__subtitle"})
        description = unicodedata.normalize("NFKD", subtitle.get_text())

        article_url = self.base_url_elComercio + title.get('href')
        img_src, time = self.get_internal_data(article_url)


        return {
            "time": time,
            "title": title.get_text(),
            "img_src": img_src,
            "subtitle": description,
            "article_url": article_url
        }


    def get_internal_data(self, article_url):
        article_soup = website_fetcher(article_url)
        try:
            picture = article_soup.find("picture")
            img = picture.find(
                "source", {"media": "(max-width: 320px)"}).get('srcset')
        except:
            img = ""
        time = article_soup.find("time").get("datetime")

        return img, time

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
