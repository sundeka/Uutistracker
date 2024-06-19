import requests
import re
from lxml import html
from typing import List
from ..abstractions.feedhandler import FeedHandler
from ..abstractions.apiresponse import APIResponse
from ..endpoints import YLE
from datetime import datetime

class Yle(FeedHandler):
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
        r = requests.get(YLE, timeout=10)
        content_str = r.content.decode("utf-8")
        html_tree = html.fromstring(content_str)
        news_blocks = html_tree.xpath("//time/../..")
        raw_headlines = []
        for block in news_blocks:
            props = {}
            props["id"] = block.text_content()
            props["headline"], props["time"] = self._clean_headline(block.text_content())
            raw_headlines.append(props)
        return raw_headlines
    
    def parse(self, entry) -> APIResponse:
        time_str = entry["time"].split(":")
        now = datetime.now()
        time = datetime(now.year, now.month, now.day, int(time_str[0]), int(time_str[1]), 0)
        return APIResponse(entry["id"], "YLE", entry["headline"].replace("\xad", ""), time)

    def _clean_headline(self, input_string: str):
        time_pattern = r'(\d{1,2}:\d{2})'
        time_match = re.search(time_pattern, input_string)
        time = time_match.group(1)
        headline = input_string[:time_match.start()].strip()
        return headline, time