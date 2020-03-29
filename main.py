from extractor import Extractor


class NewScrapper(Extractor):
    def __init__(self, diary="all", limit=3):
        self.diary = diary
        self.limit = limit
        self.selected_daily = self.select_daily(diary)

    def get_news(self):
        articles = self.get_articles(self.selected_daily, self.limit)
        return articles


if __name__ == "__main__":
    x = NewScrapper("correo")
    test = x.get_news()
    print(test)
