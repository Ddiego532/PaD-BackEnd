# TODO: Acortar esto.
from .helpers import is_absolute, get_joined_url, get_filename_by_domain, create_json_file
from requests import Response
from .news_data_handler import NewsDataFinder
# only for fixing helpers args.
from .news_soup import NewsSoup, Tag

def remove_multiple_irrelevant_data(tag_element : Tag, criteria : dict):
    bad_content : dict = criteria.get("irrelevant_tags", None)

    # not removed.
    if bad_content is None:
        return False
    
    tags = bad_content["tags"]
    classes = bad_content["classes"]

    tag_count = len(tags)

    if tag_count != len(classes):
        return False
    
    for index in range(0, tag_count):
        selected_tag = tags[index]
        class_ = classes[index]

        data = tag_element.find_all(selected_tag, {"class": class_})

        if data is None: continue

        for child in data:
            child.decompose()

    return True

class NewsSaver:
    """Guarda los datos de una noticia en memoria y pueden ser exportados a JSON."""
    def __init__(self, crit : dict, source : str):
        """
        Inicializa el objeto para poder guardar noticias.

        :params:
            crit : dict - Las etiquetas del cuerpo de una noticia, que constituye un titulo, una bajada, el contenido, la fecha, las etiquetas.
            
            source : str - La URL fuente, este parametro se usa por defecto para darle nombre al archivo JSON.
        """
        self.news_selector = crit
        self.source_url = source
        self.saved_data = list()
        self.filename = f"{get_filename_by_domain(self.source_url)}_latest_news"

    def set_filename(self, filename : str):
        """
        Cambia el nombre del archivo JSON al momento de exportar datos.

        :params:
            filename : str - Nuevo nombre de archivo.
        """
        self.filename = filename

    def _save_primary_data(self, data : dict, finder: NewsDataFinder):
        """
        Guarda datos primarios como el titulo, el sub-titulo, y la fecha.

        :params:
            data : dict - El diccionario para guardar los datos de la noticia.
        
            finder : NewsDataFinder - El objeto de buscador de datos de noticia.

        :returns:
            bool - Indica si la noticia es válida para poder proseguir guardandola.
        """
        title = finder.find_title()
        # this may be present sometimes.
        subtitle = finder.find_subtitles()
        date = finder.find_date()

        if not (title or date):
            print(f"The requested news doesn't have a ", "title." if title is None else "date.")
            return False
        
        data["title"] = title
        data["subtitle"] = subtitle
        data["date"] = date

        return True
    
    def _save_multimedia(self, data : dict, finder : NewsDataFinder):
        """
        Guarda los datos multimedia de una noticia, en este caso solamente guarda la imagen.

        :params:
            data : dict - Diccionario donde guardar la noticia.
            finder : NewsDataFinder - El objeto buscador de datos de una noticia.
        """
        # check if exists on meta first.
        image = finder.find_representative_image(self.source_url)

        if image:
            data["image"] = image

    def __extract_content(self, soup : NewsSoup):
        """
        Extrae el contenido para luego intentar guardarlo en los datos.

        :params:
            soup : NewsSoup - El parser HTML de la noticia.

        :returns:
            content_text : str - El contenido de la noticia.
        """
        content_node = soup.find_tag_by_criteria(self.news_selector["content"])

        if content_node is None:
            return None

        content_text = ""

        # to extract it properly we should remove the unneeded data like ads or something.
        remove_multiple_irrelevant_data(content_node, self.news_selector)

        # extract paragraphs, headings, etc...
        for elem in content_node.find_all(recursive=False):
            if elem is None: continue

            text = elem.get_text(strip=True)
            content_text += text

        return content_text

    def _save_content(self, data : dict, soup : NewsSoup):
        """
        Guarda el cotenido de una noticia en los datos.

        :params:
            data : dict - Los datos donde insertar el contenido.
            soup : NewsSoup - El parser de la noticia.

        :returns:
            check : bool - Si los datos se han podido guardar de manera correcta.
        """
        # could be images or video.
        content = self.__extract_content(soup)

        if not content:
            print("There is no content to save. Nullifying saving...")
            return False

        # append this data to dictionary.
        data["content"] = content

        return True

    def _save_misc_data(self, data : dict, finder : NewsDataFinder, page_source : str = ""):
        """
        Guarda datos miscelaneos de una pagina, como la fuente, el link completo de la fuente y las etiquetas.

        :params:
            data : dict - Diccionario para poder guardar los datos.
            finder: NewsDataFinder - Buscador del contenido de una noticia.
            page_source : str - La fuente de la página.
        """
        # where it comes.
        data["source"] = self.source_url
        data["full_source"] = page_source

        tags = finder.find_tags()

        if tags and len(tags) > 0:
            data["tags"] = tags

    # retrieve this data first and then dump it.
    # TODO: change the parameter data type.
    def save_to_dict(self, conn_data : Response):
        """
        Guarda los datos solicitados de la pagina en un diccionario basados en el criterio especificado.

        :params:
            conn_data : Response - La response para poder realizar operaciones correspondientes.
        """
        # the stuff we save here.
        news_data = dict()
        soup = NewsSoup(markup=conn_data.text, from_encoding="utf-8")

        # important thing if we want to get the proper data.
        finder = NewsDataFinder(soup, self.news_selector)

        # can't save.
        if not self._save_primary_data(news_data, finder) or not self._save_content(news_data, soup):
            print(f"The {conn_data.url} news can't be saved.")
            return

        self._save_multimedia(news_data, finder)
        self._save_misc_data(news_data, finder, conn_data.url)
        self.saved_data.append(news_data)

    def get_saved_data(self):
        """
        Obtiene los datos de todas las noticias scrapeadas en formato diccionario.
        
        :returns:
            saved_data : dict - Los datos.
        """
        return self.saved_data

    def save_to_json(self): 
        create_json_file(self.filename, self.saved_data)