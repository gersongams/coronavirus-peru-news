import unicodedata

from utils import extract_articles, format_time, website_fetcher


class LaRepublicaScrapper():
    diary = "La República"
    diary_id = "la_republica"
    base_url_laRepublica = "https://larepublica.pe"
    url_coronavirus_news = "https://larepublica.pe/tag/coronavirus-en-peru/"
    soup = []
    articles = []
    articles_soup = []

    def __init__(self, limit = 5):
        self.limit = limit

    def fetch_news(self):
        self.soup = website_fetcher(self.url_coronavirus_news)

    def fetch_articles(self):
        articles_soup = self.soup.findAll("article", {"class": "PostSection"})
        self.articles_soup = articles_soup[:self.limit]

    def get_data_from_articles(self, story):
        time = story.find("span", {"class": "PostSectionListSPAN"})
        title = story.find("a", {"class": "PostSectionListA"})
        subtitle = story.find("p", {"class": "PostSectionContent"})
        description = unicodedata.normalize("NFKD", subtitle.get_text())

        article_url = self.base_url_laRepublica + title.get('href')
        return {
            "time": format_time(time.get_text()),
            "title": title.get_text(),
            "img_src": self.get_internal_image(article_url),
            "subtitle": description,
            "article_url": article_url
        }

    def get_internal_image(self, article_url):
        article_soup = website_fetcher(article_url)
        try:
            picture = article_soup.find("picture")
            img = picture.find("source", {"media": "(max-width: 320px)"})
            return img.get('srcset')
        except:
            img = article_soup.find("meta",  property="og:image")
            return img.get('content')

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
