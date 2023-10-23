from html_scraper import HTMLScraper
from criterias import *

EXAMPLE_LEVEL = 5

teletrece = HTMLScraper(TELETRECE)
teletrece.start_scraping(EXAMPLE_LEVEL)
teletrece.news_saver.save_to_json()