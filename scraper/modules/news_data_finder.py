from .news_soup import NewsSoup
from .helpers import get_tags_from_str

class NewsDataFinder:
    def __init__(self, soup : NewsSoup, selector : dict):
        self.soup = soup
        self.selector = selector

    def find_tags(self):
        """
        Encuentra las etiquetas de una noticia.

        :returns:
            tags : list - Las etiquetas.
        """
        meta = self.soup.get_meta_content("name", "keywords")

        if meta:
            return get_tags_from_str(meta)
        
        # use the tags criteria.
        tags = self.selector.get("news_tags")
    
        if not tags:
            print("This page doesn't have any tags.")
            return

        tag_element = self.soup.find_tag_by_criteria(tags)

        if not tag_element:
            return
        
        cleaned_tags = []
        
        for refs in tag_element.find_all("a"):
            text : str = refs.get_text(strip=True)
            if len(text) <= 0 or ("..." in text): continue
            # clean text.
            no_seps = text.replace("|", "")
            no_hashtags = no_seps.replace("#", "")
            cleaned_text = no_hashtags.lower().strip()

            cleaned_tags.append(cleaned_text)

        return cleaned_tags

    def find_text_data_element(self, elem : str) -> str:
        """
        Encuentra los elementos especificados en el text_data.

        :params:
            elem : str - Elemento del text_data.
        
        :returns:
            content : str - El contenido del elemento especificado.
        """
        text_data : dict = self.selector["text_data"]

        if not text_data:
            raise ValueError("text_data tag attributes can't be None.")
        
        value = text_data.get(elem, None)

        # not found so bye bye.
        if not value:
            return

        textelem = self.soup.find_tag_by_criteria(value)

        # prolly a tag.
        if textelem:
            if hasattr(textelem, "text"):
                textelem = textelem.text

            textelem = textelem.strip()

        return textelem
    
    def find_representative_image(self):
        """
        Encuentra una imagen representativa de una noticia.

        :returns:
            source : str - La fuente de la imagen en formato relativo o absoluto.
        """
        source = self.soup.get_meta_og_content("image")

        # not on meta, so use the tags.
        if not source:
            image_data : dict = self.selector["image_url"]
            
            # get data.
            image = self.soup.find_tag_by_criteria(image_data)
            if not image: return
        
            # get source.
            source = image.get(image_data.get("forced_src", "src"))

        return source
    
    def find_title(self):
        return self.find_text_data_element("title")

    def find_subtitles(self):
        return self.find_text_data_element("subtitle")
    
    def find_date(self):
        return self.find_text_data_element("date")


