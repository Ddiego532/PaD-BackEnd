from modules.helpers import create_session, handle_session, get_base_url
from modules.news_saver import NewsSaver
from modules.robots_parser import RobotsParser

# PARENT CLASS.
class BaseScraper:
    def __init__(self, criteria : dict) -> None:
        """
        Especifica el criterio para el scraper.

        :params:
            criteria : dict - Los parametros del criterio en formato llave-valor.

            Los parametros del criterio son los siguientes:
                url : str - URL para obtener los enlaces.
                forbidden_paths : list - Rutas a los que no se debe scrapear.
                news_selector : dict - El selector para poder obtener los datos de una noticia.
        """
        # private thing as we are scraping based on this.
        # protected as childs require it.
        self._criteria = criteria
        self.url = criteria.get("url", None)

        self.conn_delay = 0

        # should be like latercera.cl/
        self.seed_url = get_base_url(self.url)

        # try catch goofy aaa thing.
        if self.seed_url is None:
            raise ValueError(f"The seed URL has a null value.")

        self.page_session = create_session()
        self.cached_links = set()

        # imagine using this, but we are doing it for the xml.
        self.__robot_parser = RobotsParser(self.seed_url, self.page_session)
        self.news_saver = NewsSaver(self._criteria["news_selector"],  self.seed_url)

    def set_connection_delay(self, delay : int):
        """
        Cambia el delay de conexión para cada request.

        :params:
            delay : int -  El nuevo delay.
        """
        self.conn_delay = delay
    
    def is_forbidden_sublink(self, link : str) -> bool:
        """
        Revisa si el sub-enlace es una ruta a la que se no debe guardar.

        :params:
            link : str - El sub-enlace.

        :returns:
            check : bool - El sub-enlace es una ruta prohibida.
        """
        forbidden_paths = self._criteria.get("forbidden_paths", [])
    
        return any(path in link for path in forbidden_paths)
    
    def handle_page_session(self, url : str, mode : str = "get", **kwargs):
        """
        Maneja las sesiones de una pagina para poder scrapearla.

        :params:
            url : str - El URL en cuestion.
            mode : str - Modo HTTP para realizar peticiones, solamente soporta GET y POST.
            kwargs : any - Argumentos variables para las peticiones.

        :return:
            resp : Response - La respuesta del servidor.
        """
        return handle_session(self.page_session, url=url, delay=self.conn_delay, mode=mode, **kwargs)

    def save_news(self):
        """
        Guarda las noticias en el objeto NewsSaver con los enlaces obtenidos.
        """
        news_link : str

        for news_link in self.cached_links:
            conn = self.handle_page_session(url=news_link)
            if not conn: continue

            self.news_saver.save_to_dict(conn)

        print("Finished saving news in memory.")

    def get_news_saver(self):
        """
        Retorna el objeto NewsSaver el cual se encarga de guardar las noticias sde los subenlaces.

        :returns:
            news_saver : NewsSaver - El objeto NewsSaver.
        """
        return self.news_saver

    # force to go to a single url.
    def _connect_and_add_sublinks(self, url : str):
        """
        Conecta y agrega sub-enlaces de noticias.

        :params:
            url : str - El enlace especificado en el criterio o un sub-enlace.
        """
        pass

    def get_sublinks_singlepage(self):
        return self._connect_and_add_sublinks(self.url)

    # this could vary in terms of fetching.
    def get_links_by_exploring(self, max_level : int = 1):
        """
        Obtiene los enlaces utilizando la páginación especificada.

        :params:
            max_level : int - El numero máximo de exploraciones que se deben hacer.
        """
        pass

    def start_scraping(self, level : int = 1):
        """
        Comienza a scrapear y guarda las noticias.

        :params:
            level : int - El nivel máximo de exploración.
        """
        self.get_links_by_exploring(level)
        self.save_news()

    def get_news_links(self) -> set:
        """
        Obtiene los sub-enlaces obtenidos en el scraping.

        :returns:
            cached_links : set - Los links en memoria.
        """
        return self.cached_links
        
    def get_links_by_sitemap(self):
        pass

    def get_sitemaps(self) -> list:
        """
        Obtiene los sitemaps utilizando el RobotsParser.

        :returns:
            sitemaps : list - Los sitemaps.
        """
        # can return none.
        return self.__robot_parser.get_sitemaps()