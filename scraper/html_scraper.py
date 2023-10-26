from base_scraper import BaseScraper
from modules.news_soup import NewsSoup
from modules.helpers import is_valid, is_absolute

# hrefs we don't care.
BAD_HREFS = {"#", "_blank", "javascript:void(0)"}

# is there something more we can do?
class HTMLScraper(BaseScraper):
    """
    Scrapea contenido de los HTML.
    """
    def __init__(self, criteria: dict) -> None:
        """
        Usa los mismos criterios que el padre, pero ahora necesita el tag especifico.

        Criterios para el diccionario: 
            tag : str - La etiqueta especifica en donde se obtienen los enlaces.
            identifier_attrib : str -  El atributo que identifica a esa etiqueta.
            attrib_value : str - El valor del atributo identificador.
            force_spec_url: bool - Forzar al URL principal a ser scrapeado.
            explore_paths : str | None - Las ruta que contiene la páginación. Se especifica el page_num.
        """
        super().__init__(criteria)

        self.target_tag = criteria.get("tag", None)

    def _get_from_url(self):
        """
        Obtiene los enlaces del URL especificado, solamente si la páginación es muy especifica.
        """
        if not self._criteria.get("force_spec_url", False):
            return
        
        print("Connecting to the URL specified:", self.url)

        self._connect_and_add_sublinks(self.url)

    def get_links_by_exploring(self, max_level: int = 1):
        # only a hotfix for as.com
        self._get_from_url()

        explore_path = self._criteria.get("explore_path", None)
    
        if explore_path is None: 
            return self.get_sublinks_singlepage()
        
        # below 1 bad!!!
        max_level = max(max_level, 1)

        fullpath = f"{self.seed_url}/{explore_path}"

        for i in range(1, max_level + 1):
            numpath = fullpath.replace("page_num", str(i), 1)
           #  print("Going to: ", numpath)
            self._connect_and_add_sublinks(numpath)

        return super().get_links_by_exploring(max_level)
    
    def _connect_and_add_sublinks(self, url: str):
        print("Passed URL: ", url)
        conn = self.handle_page_session(url=url)
        soup = NewsSoup(conn.text)

        element = soup.find_element_by_identifier_attribute(self._criteria)
    
        for link in element.find_all("a"):
            href = link.get("href")

            if (href is None) or (href in BAD_HREFS) or self.is_forbidden_sublink(href):
                print("Bad or forbidden href: ", href)
                continue

            if not is_absolute(href):
                href = f"{self.seed_url}{href}"
            
            # doesn't match with the seed url.
            if not is_valid(href, self.seed_url): 
                print("Link is not valid, href: ", href)
                continue

            print("Sublink: ", href)

            self.cached_links.add(href)