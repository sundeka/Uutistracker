from typing import List, Iterable
from .apiresponse import APIResponse
import logging
from lxml import html
from datetime import datetime

class ScraperHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_articles() -> List[APIResponse]:
        """The main driver function that calls the other functions."""
        pass

    def get_html_tree() -> html.HtmlElement:
        """Request the HTML page and turn it into an HtmlElement object 
        using the html.fromstring() method."""
        pass

    def get_news_blocks(html_tree: html.HtmlElement) -> Iterable[html.HtmlElement]: 
        """From the HTML tree, parse the indivudal news blocks into an iterable."""
        pass

    def parse_headline(block: html.HtmlElement) -> str:
        """Parse the headline text from the news block."""
        pass

    def parse_time(block: html.HtmlElement) -> datetime:
        """Parse the time from the news block."""
        pass