import json
from multiprocessing import Pipe, Process

from lib.correo_scrapper import CorreoScrapper
from lib.elComercio_scrapper import ElComercioScrapper
from lib.laRepublica_scrapper import LaRepublicaScrapper
from lib.peru21_scrapper import Peru21Scrapper
from lib.rpp_scrapper import RPPScrapper


class Extractor():
    articles = []
    limit = 3
    diary = ''

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

        self.diary = newspapers.get(diary, "Diario seleccionado invalido")
        return self.diary

    def scrape_articles(self, selected_daily, limit):
        scrapper = None
        self.limit = limit
        scrappers = [
            ElComercioScrapper,
            LaRepublicaScrapper,
            RPPScrapper,
            Peru21Scrapper,
            CorreoScrapper
        ]
        if selected_daily == "el_comercio":
            scrapper = scrappers[0](limit)
        if selected_daily == "la_republica":
            scrapper = scrappers[1](limit)
        if selected_daily == "rpp":
            scrapper = scrappers[2](limit)
        if selected_daily == "peru21":
            scrapper = scrappers[3](limit)
        if selected_daily == "correo":
            scrapper = scrappers[4](limit)

        if type(selected_daily) is dict:
            parents=[]
            results=[]
            processes=[]

            for i in scrappers:
                parent_conn, child_conn = Pipe()
                process = Process(target=self.parallel_scrapper, args=(i,child_conn,))
                processes.append(process)
                results.append(parent_conn)

            for process in processes: process.start()
            self.articles = [res.recv() for res in results]
            for process in processes: process.join()

        else:
            data = scrapper.get_articles()
            self.articles.append(data)

    def parallel_scrapper(self, diary, conn):
        scrapper = diary(self.limit)
        data = scrapper.get_articles()
        conn.send(data)
        conn.close()

    def get_articles(self, selected_daily, limit):
        self.scrape_articles(selected_daily, limit)
        return self.articles
