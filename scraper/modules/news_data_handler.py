from .news_soup import NewsSoup

# omg a new class moment
class NewsDataFinder:
    def __init__(self, soup : NewsSoup, selector : dict):
        self.soup = soup
        self.selector = selector

    def find_text_data_element(self, elem : str):
        text_data = self.selector["text_data"]

        if not text_data:
            raise ValueError("text_data tag attributes can't be None.")
        
        value = text_data[elem]
        textelem = self.soup.find_tag_by_criteria(value)

        # prolly a tag.
        if textelem and hasattr(textelem, "text"):
            textelem = textelem.text

        return textelem
    
    def find_title(self):
        return self.find_text_data_element("title")

    def find_subtitles(self):
        return self.find_text_data_element("subtitle")
    
    def find_date(self):
        return self.find_text_data_element("date")


