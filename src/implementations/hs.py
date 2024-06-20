import requests
import re
from lxml import html
from typing import List, Iterable
from ..abstractions.scraperhandler import ScraperHandler
from ..abstractions.apiresponse import APIResponse
from ..exceptions.expectedfaultyheadline import ExpectedFaultyHeadlineException
from ..endpoints import HS
from datetime import datetime

class Helsinginsanomat(ScraperHandler):
    def __init__(self):
        super().__init__()

    def get_articles(self) -> List[APIResponse]:
        articles = []
        html_tree = self.get_html_tree()
        for block in self.get_news_blocks(html_tree):
            id = block.text_content()
            try:
                headline = self.parse_headline(block)
            except ExpectedFaultyHeadlineException:
                continue
            time = self.parse_time(block)
            articles.append(APIResponse(
                id,
                "HS",
                headline,
                time
            ))
        return articles

    def get_html_tree(self) -> html.HtmlElement:
        r = requests.get(HS, timeout=10)
        content_str = r.content.decode("utf-8")
        return html.fromstring(content_str)
    
    def get_news_blocks(self, html_tree: html.HtmlElement) -> Iterable[html.HtmlElement]:
        return html_tree.xpath("//a[@class='block' and starts-with(@href, '/')]")
    
    def parse_headline(self, block: html.HtmlElement) -> str:
        text = block.text_content()
        headline = ""
        # Remove everything before the pipe (|) including the pipe
        text = re.sub(r'^.*\|', '', text)    
        text = text.replace('Tilaajille', '')
        # Separate the headline from the time
        match = re.search(r'(\d{1,2}:\d{2})$', text)
        if match:
            headline = text[:match.start()].strip()
        elif "uutisvinkki" in text:
            raise ExpectedFaultyHeadlineException()
        else:
            self.logger.exception(f"No match: {text}")
        return headline.replace("\xad", "")

    def parse_time(self, block: html.HtmlElement) -> datetime:
        time = datetime.now()
        text = block.text_content()
        match = re.search(r'(\d{1,2}:\d{2})$', text)
        if match:
            time_str = match.group(0)
            time = datetime(time.year, time.month, time.day, int(time_str.split(":")[0]), int(time_str.split(":")[1]), 0)
        return time