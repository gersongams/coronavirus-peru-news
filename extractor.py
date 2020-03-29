from elComercio_scrapper import ElComercioScrapper
from laRepublica_scrapper import LaRepublicaScrapper
from rpp_scrapper import RPPScrapper
from peru21_scrapper import Peru21Scrapper
from correo_scrapper import CorreoScrapper
import json


class Extractor():
    articles = []

    def select_daily(self, diary):
        newspapers = {
            "el_comercio": 'el_comercio',
            "la_republica": 'la_republica',
            "rpp": 'rpp',
            "peru21": "peru21",
            "correo": "correo"
        }

        if diary == "all":
            return newspapers

        return newspapers.get(diary, "Diario seleccionado invalido")

    def scrape_articles(self, selected_daily, limit):
        scrapper = None
        if selected_daily == "el_comercio":
            scrapper = ElComercioScrapper(limit)
        if selected_daily == "la_republica":
            scrapper = LaRepublicaScrapper(limit)
        if selected_daily == "rpp":
            scrapper = RPPScrapper(limit)
        if selected_daily == "peru21":
            scrapper = Peru21Scrapper(limit)
        if selected_daily == "correo":
            scrapper = CorreoScrapper(limit)

        if type(selected_daily) is dict:
            print("ALL_IN")
        else:
            data = scrapper.get_articles()
            self.articles.append(data)

    def get_articles(self, selected_daily, limit):
        self.scrape_articles(selected_daily, limit)
        response = {
            "status": "OK",
            "data": self.articles
        }
        return json.dumps(response, ensure_ascii=False)
