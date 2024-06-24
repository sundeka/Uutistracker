from lxml import html
from datetime import datetime
from src.implementations.yle import Yle
from src.implementations.hs import Helsinginsanomat

class MockHtmlElement:
    def __init__(self, text: str = None):
        self.text = text

    def text_content(self) -> str:
        return self.text
    
    def getchildren(self):
        return [self, self]

def test_get_html_tree():
    yle = Yle()
    hs = Helsinginsanomat()
    for platform in [yle, hs]:
        tree = platform.get_html_tree()
        assert type(tree) == html.HtmlElement

def test_get_news_blocks():
    yle = Yle()
    hs = Helsinginsanomat()
    for platform in [yle, hs]:
        tree = platform.get_html_tree()
        blocks = platform.get_news_blocks(tree)
        assert iter(blocks)
        assert type(blocks[0]) == html.HtmlElement

def test_parse_headline():
    hs = Helsinginsanomat()
    hs_html = MockHtmlElement("this is a test \xadheadline12:08")
    yle = Yle()
    yle_html = MockHtmlElement("this is a test \xadheadline")
    for platform, element in [(yle, yle_html), (hs, hs_html)]:
        headline = platform.parse_headline(element)
        assert headline == "this is a test headline"

def test_parse_time():
    hs = Helsinginsanomat()
    hs_html = MockHtmlElement("this is a test \xadheadline12:08")
    yle = Yle()
    yle_html = MockHtmlElement("asdasd12:08Politiikka")
    for platform, element in [(yle, yle_html), (hs, hs_html)]:
        now = datetime.now()
        time = datetime(now.year, now.month, now.day, 12, 8, 0)
        time_parsed = platform.parse_time(element)
        assert time == time_parsed