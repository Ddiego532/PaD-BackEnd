from util import is_valid, create_conn, get_decoded_text
from bs4 import BeautifulSoup

LOOP_DELAY = 1

# should provide criterias varying on the website.
class Scrapper:
    def __init__(self, url : str, criteria : dict = {}):
        # Starting url.
        self.url = url
        self.seed_url = url

        # Initialize voidly?.
        self.root_content = None

        # this is for recursive algo only.
        self.cached_urls = set()

        self._start_connection()

    def _start_connection(self):
        resp = create_conn(self.url)

        # generic exception.
        if resp is None:
            raise Exception("Can't connect.")
        
        self.root_content = resp.content
        
        # conn was posible.
        return True
    
    def get_articles_links(self):
        # should work for la tercera.
        soup = BeautifulSoup(self.root_content, "html.parser", from_encoding="UTF-8")
        
        for articles in soup.find_all("article"):
            link_elem = articles.find("a", href=True)
            if link_elem is None: continue
            real_link = link_elem.get("href")

            yield real_link

    def get_news_on_articles(self, delay : float = 0):
        for link in self.get_articles_links():
            # visited this. don't do it again.
            if link in self.cached_urls: 
                continue

            sub_conn = create_conn(link, delay)

            # no connection, continue...
            if not sub_conn:
                print(f"Can't connect to {link}, because: {sub_conn.status_code}")
                continue

            # return into a text.
            sub_conn = sub_conn.text
    
            soup = BeautifulSoup(sub_conn, "html.parser")
            news = soup.find("article", {"class" : "post"})

            # prolly not valid news.
            if not news: continue

            # HACK: Put this thing an encoding without the BS4 method as it throws an unicode error.
            news_text = news.get_text()
            self.cached_urls.add(link)
            
            yield news_text
        
    def scrape_news(self):
        self._start_connection()
