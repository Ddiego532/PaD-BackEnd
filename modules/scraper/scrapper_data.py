from helpers import create_conn, get_element_by_id_or_class, get_tag, is_absolute, get_joined_url
# only for fixing helpers args.
from bs4 import BeautifulSoup, Tag
import json

def remove_irrelevant_data(tag_element : Tag, criteria : dict):
    bad_content : dict = criteria.get("common_irrelevant_tag", None)

    # not removed.
    if bad_content is None:
        return False
    
    tag = bad_content["tag"]
    class_id = bad_content["class"]

    data = tag_element.find_all(tag, {"class" : class_id})
    
    if data is not None:
        for child in data:
            child.decompose()

    return True

# basically a robots.txt checker.
class RobotsParser:
    def __init__(self, url):
        self.__base_url = url
        # self.disallowed_links : list = None
        self.site_data = {}
        self.__request_data()

    def __request_data(self) -> None:
        robots_txt = create_conn(f"{self.__base_url}/robots.txt", 0)

        # FIXME: There are some sites without this file, so we need to add a better check.
        if not robots_txt:
            raise Exception("Can't fetch robots.txt")
        
        text_content = robots_txt.text
        stripped_newlines = text_content.splitlines()

        for data in stripped_newlines:
            # no need to iterate.
            if len(data) <= 0 or data.startswith("#"): continue

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
        return self.site_data.get("Disallow", None)
    
    def get_sitemaps(self) -> list:
        return self.site_data.get("Sitemap", None)
    
    def get_user_agents(self) -> list:
        return self.site_data.get("User-agent", None)
    
    def get_site_data(self) -> dict:
        return self.site_data

class NewsSaver:
    def __init__(self, crit : dict, source : str):
        self.news_selector = crit
        self.source_url = source
        self.saved_data = list()

    def set_filename(self):
        pass

    # really considering those 2 as an attribute.
    # this is the most important one.
    def _save_primary_data(self, data : dict, soup : BeautifulSoup):
        text_data = self.news_selector["text_data"]

        # iterate the text stuff.
        for key in text_data:
            # special handler.
            # we dont care about these ones.
            value : dict = text_data[key]
            element = get_element_by_id_or_class(value, soup)

            # not a news page.
            if element is None: 
                return False

            text = element.text
            data[key] = text.strip()

        return True
    
    def _save_multimedia(self, data : dict, soup: BeautifulSoup):
        image = get_tag(self.news_selector["image_url"], soup)
        if not image: return
    
        # get source.
        source = image.get("src")
        
        # get the absolute path.
        if not is_absolute(source):
            source = get_joined_url(self.source_url, source)

        data["image"] = source

    def _save_content(self, data : dict, soup : BeautifulSoup):
        sel = self.news_selector
        
        # could be images or video.
        self._save_multimedia(data, soup)
    
        # here we save the content.
        content = get_element_by_id_or_class(sel["content"], soup)
        content_text = ""

        remove_irrelevant_data(content, sel)

        for elem in content.find_all(recursive=False):
            if elem is None: continue

            text = elem.get_text(strip=True)
            content_text += text

        # append this data to dictionary.
        data["content"] = content_text.strip()

    def _save_misc_data(self, data : dict, soup : BeautifulSoup):
        # where it comes.
        sel = self.news_selector
        data["source"] = self.source_url
    
        # the tags.
        news_tags = sel["news_tags"]
        if not news_tags: return

        element = get_element_by_id_or_class(news_tags, soup)

        if not element: return
        data["tags"] = []
    
        for refs in element.children:
            text = refs.get_text(strip=True)
            if len(text) <= 0: continue

            data["tags"].append(text.lower())

    # retrieve this data first and then dump it.
    def save_to_dict(self, soup : BeautifulSoup):
        # the stuff we save here.
        news_data = dict()

        if not self._save_primary_data(news_data, soup):
            return
        
        self._save_content(news_data, soup)
        self._save_misc_data(news_data, soup)

        self.saved_data.append(news_data)

    def save_to_json(self, clear_data : bool = True): 
        with open("test.json", "w", encoding="utf-8") as json_file:
            json.dump(self.saved_data, json_file, ensure_ascii=False, indent=4)

        if clear_data:
            self.saved_data.clear()