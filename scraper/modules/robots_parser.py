# basically a robots.txt checker.
class RobotsParser:
    """
    Parser del archivo robots.txt de un sitio web.
    """
    def __init__(self, url : str, parent_session):
        """
        Inicializa el parser.

        :params:
            url : str - La URL base para poder encontrar el archivo.
            parent_session : Session - La sesion del padre para poder realizar peticiones.
        """
        self.__base_url = url
        # self.disallowed_links : list = None
        self.site_data = {}
        self.parent_session = parent_session
        self.__request_data()

    def __request_data(self) -> None:
        """
        Solicita los datos del robots.txt del sitio.
        """
        robots_txt = self.parent_session.get(f"{self.__base_url}/robots.txt")

        # FIXME: There are some sites without this file, so we need to add a better check.
        if not robots_txt:
            raise Exception("Can't fetch robots.txt")
        
        text_content : str = robots_txt.text
        stripped_newlines = text_content.splitlines()

        for data in stripped_newlines:
            # no need to iterate.
            if len(data) <= 1 or data.startswith("#"): continue
            # split one only.
            mapped = data.split(":", 1)

            # this is the thing we need.
            key = mapped[0]

            # we don't care about this.
            if key == "Allow": continue
            value = mapped[1].strip()

            if not key in self.site_data:
                self.site_data[key] : list = []

            self.site_data[key].append(value)

    def get_disallowed_links(self) -> list:
        """
        Obtiene los enlaces relativos no permitidos.

        :returns:
            links : list - Enlaces prohibidos.
        """     
        return self.site_data.get("Disallow", None)
    
    def get_sitemaps(self) -> list:
        """
        Obtiene los sitemaps especificados.

        :returns:
            links : list - Los sitemaps.
        """
        return self.site_data.get("Sitemap", None)
    
    def get_user_agents(self) -> list:
        """
        Obtiene los agentes de usuario especificados en el archivo.

        :returns:
            user_agents : list - Agentes de usuario.
        """
        return self.site_data.get("User-agent", None)
    
    def get_site_data(self) -> dict:
        """
        Obtiene todos los datos del robots.txt (exceptuando el Allow).

        :returns:
            data : dict - Datos del robots.txt.
        """
        return self.site_data
