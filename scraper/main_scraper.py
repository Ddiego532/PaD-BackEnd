from html_scraper import HTMLScraper
from modules.helpers import create_json_file
from criterias import *

EXAMPLE_LEVEL = 1
LIST_OF_SOURCES = [TELETRECE, ELDINAMO, ELMOSTRADOR, CNNCHILE, TVN_NOTICIAS,
                BIOBIOCHILE, LATERCERA, MEGANOTICIAS, ASCOM, COOPERATIVA, ADNCL]

ref_list = []

for webpage in LIST_OF_SOURCES:
    scrapper_obj = HTMLScraper(webpage)
    scrapper_obj.start_scraping()

    news_saver = scrapper_obj.get_news_saver()

    ref_list.extend(news_saver.get_saved_data())

create_json_file("all_news", ref_list)