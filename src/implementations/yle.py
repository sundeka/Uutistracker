import requests
import re
from lxml import html
from typing import List, Iterable
from ..abstractions.scraperhandler import ScraperHandler
from ..abstractions.apiresponse import APIResponse
from ..endpoints import YLE
from datetime import datetime

class Yle(ScraperHandler):
    def __init__(self):
        super().__init__()

    def get_articles(self) -> List[APIResponse]:
        articles = []
        html_tree = self.get_html_tree()
        for block in self.get_news_blocks(html_tree):
            id = block.text_content()
            headline = self.parse_headline(block)
            time = self.parse_time(block)
            articles.append(APIResponse(
                id,
                "YLE",
                headline,
                time
            ))
        return articles

    def get_html_tree(self) -> html.HtmlElement:
        r = requests.get(YLE, timeout=10)
        content_str = r.content.decode("utf-8")
        return html.fromstring(content_str)
    
    def get_news_blocks(self, html_tree: html.HtmlElement) -> Iterable[html.HtmlElement]:
        return html_tree.xpath("//time/../..")
    
    def parse_headline(self, block: html.HtmlElement) -> str:
        return block.getchildren()[0].text_content().replace("\xad", "")

    def parse_time(self, block: html.HtmlElement) -> datetime:
        time = datetime.now()
        time_pattern = r'(\d{1,2}:\d{2})'
        time_match = re.search(time_pattern, block.getchildren()[1].text_content())
        if time_match:
            time_str = time_match.group(1)
            time = datetime(time.year, time.month, time.day, int(time_str.split(":")[0]), int(time_str.split(":")[1]), 0)
        return time