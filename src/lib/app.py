import json
import time

from lib.extractor import Extractor


class NewScrapper(Extractor):
    def __init__(self, diary="all", limit=3):
        self.diary = diary
        self.limit = limit
        self.selected_daily = self.select_daily(diary)

    def get_news(self):
        articles = self.get_articles(self.selected_daily, self.limit)
        return articles

# if __name__ == "__main__":
#     start_time = time.time()
#     scrapper = NewScrapper("all")
#     data = scrapper.get_news()
#     print("--- %s seconds ---" % (time.time() - start_time))
#     ss = json.dumps(data)
#     print(data)
#     with open('test.json', 'w') as f:
#         print(ss, file=f)  # Python 3.x
