import requests
import re
from lxml import html
from typing import List
from ..abstractions.feedhandler import FeedHandler
from ..abstractions.apiresponse import APIResponse
from ..endpoints import HS
from datetime import datetime

class Helsinginsanomat(FeedHandler):
    def __init__(self):
        super().__init__()

    def get_articles(self) -> List[APIResponse]:
        articles = []
        try:
            data = self.fetch()
        except TimeoutError:
            self.logger.error("Request timed out!")
            return articles
        except ValueError as e:
            self.logger.error(e)
            return articles
        for entry in data:
            try:
                parsed = self.parse(entry)
                articles.append(parsed)
            except TypeError as e:
                self.logger.error(e)
        return articles

    def fetch(self) -> List[dict]:
        r = requests.get(HS, timeout=10)
        content_str = r.content.decode("utf-8")
        html_tree = html.fromstring(content_str)
        news_blocks = html_tree.xpath("//a[@class='block' and starts-with(@href, '/')]")
        raw_headlines = []
        for block in news_blocks:
            props = {}
            props["id"] = block.attrib["href"]
            headline, time = self._clean_headline(block.text_content())
            if not all([headline, time]):
                continue
            props["headline"] = headline
            props["time"] = time
            raw_headlines.append(props)
        return raw_headlines
    
    def parse(self, entry) -> APIResponse:
        source = "HS"
        id = entry["id"]
        title = entry["headline"].replace("\xad", "")
        time_str = entry["time"]
        now = datetime.now()
        time = datetime(now.year, now.month, now.day, int(time_str[0]), int(time_str[1]), 0)
        return APIResponse(id, source, title, time)
    
    def _clean_headline(self, text: str):
        headline = ""
        time = []
        # Remove everything before the pipe (|) including the pipe
        text = re.sub(r'^.*\|', '', text)    
        text = text.replace('Tilaajille', '')
        # Separate the headline from the time
        match = re.search(r'(\d{1,2}:\d{2})$', text)
        if match:
            time = match.group(0).split(":")
            headline = text[:match.start()].strip()
        elif "uutisvinkki" not in text:
            self.logger.exception(f"No match: {text}")
        return headline, time