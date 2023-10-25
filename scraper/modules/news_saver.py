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
    def __init__(self, crit : dict, source : str):
        self.news_selector = crit
        self.source_url = source
        self.saved_data = list()
        self.filename = f"{get_filename_by_domain(self.source_url)}_latest_news"

    def set_filename(self, filename : str):
        self.filename = filename

    # really considering those 2 as an attribute.
    # this is the most important one.
    def _save_primary_data(self, data : dict, finder: NewsDataFinder):
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
        # check if exists on meta first.
        image = finder.find_representative_image(self.source_url)

        if image:
            data["image"] = image

    def __extract_content(self, soup : NewsSoup):
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
        # could be images or video.
        content = self.__extract_content(soup)

        if not content:
            print("There is no content to save. Nullifying saving...")
            return False

        # append this data to dictionary.
        data["content"] = content

        return True

    def _save_misc_data(self, data : dict, finder : NewsDataFinder, page_source : str = ""):
        # where it comes.
        data["source"] = self.source_url
        data["full_source"] = page_source

        tags = finder.find_tags()

        if tags and len(tags) > 0:
            data["tags"] = tags

    # retrieve this data first and then dump it.
    def save_to_dict(self, conn_data : Response):
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
        return self.saved_data

    def save_to_json(self, clear_data : bool = True): 
        create_json_file(self.filename, self.saved_data)

        if clear_data:
            self.saved_data.clear()