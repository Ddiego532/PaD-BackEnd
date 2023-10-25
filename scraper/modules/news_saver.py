# TODO: Acortar esto.
from .helpers import is_absolute, get_joined_url, get_filename_by_domain, create_json_file
from requests import Response
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
    def __init__(self, crit : dict, source : str):
        self.news_selector = crit
        self.source_url = source
        self.saved_data = list()
        self.filename = f"{get_filename_by_domain(self.source_url)}_latest_news"

    def set_filename(self, filename : str):
        self.filename = filename

    # really considering those 2 as an attribute.
    # this is the most important one.
    def _save_primary_data(self, data : dict, soup : NewsSoup):
        text_data = self.news_selector["text_data"]

        # iterate the text stuff.
        for key in text_data:
            # special handler.
            # we dont care about these ones.
            value : dict = text_data[key]
            element = soup.find_tag_by_criteria(value)

            # not a news page.
            # prolly mega noticias.
            # TODO: Refactor.
            if (element is None):
                # if subtitle empty then we go.
                if (key == "subtitle"):
                    continue
             
                return False
            
            text = element

            if hasattr(element, "text"):
                text = element.text

            data[key] = text.strip()

        return True
    
    def _save_multimedia(self, data : dict, soup: NewsSoup):
        # check if exists on meta first.
        source = soup.get_meta_content("image")

        # not on meta, so use the tags.
        if not source:
            image_data : dict = self.news_selector["image_url"]
            
            # get data.
            image = soup.find_tag_by_criteria(image_data)
            if not image: return
        
            # get source.
            source = image.get(image_data.get("forced_src", "src"))
            
            # get the absolute path.
            if not is_absolute(source):
                source = get_joined_url(self.source_url, source)

        data["image"] = source

    def _save_content(self, data : dict, soup : NewsSoup):
        sel = self.news_selector
        
        # could be images or video.
        self._save_multimedia(data, soup)
    
        # here we save the content.
        content = soup.find_tag_by_criteria(sel["content"])

        # nothing to save here.
        if content is None:
            return False

        content_text = ""

        remove_multiple_irrelevant_data(content, sel)

        for elem in content.find_all(recursive=False):
            if elem is None: continue

            text = elem.get_text(strip=True)
            content_text += text

        # append this data to dictionary.
        data["content"] = content_text

        return True

    def _save_misc_data(self, data : dict, soup : NewsSoup, page_source : str = ""):
        # where it comes.
        sel = self.news_selector
        data["source"] = self.source_url
        data["full_source"] = page_source
    
        # the tags.
        news_tags = sel.get("news_tags", None)
        if not news_tags: return

        element = soup.find_tag_by_criteria(news_tags)

        if not element: return
        data["tags"] = []

        # they are usually an href element.
        for refs in element.find_all("a"):
            text : str = refs.get_text(strip=True)
            if len(text) <= 0 or ("..." in text): continue
            # clean text.
            cleaned_text = text.replace("|", "").lower().strip()

            data["tags"].append(cleaned_text)


    # retrieve this data first and then dump it.
    def save_to_dict(self, conn_data : Response):
        # the stuff we save here.
        news_data = dict()
        soup = NewsSoup(markup=conn_data.text)

        # can't save.
        if not self._save_primary_data(news_data, soup) or not self._save_content(news_data, soup):
            return

        # self._save_content(news_data, soup)
        self._save_misc_data(news_data, soup, conn_data.url)

        self.saved_data.append(news_data)

    def get_saved_data(self):
        return self.saved_data

    def save_to_json(self, clear_data : bool = True): 
        create_json_file(self.filename, self.saved_data)

        if clear_data:
            self.saved_data.clear()