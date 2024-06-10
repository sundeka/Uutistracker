from src.implementations.iltasanomat import Iltasanomat
from src.abstractions.apiresponse import APIResponse
from datetime import datetime

#
# DON'T MODIFY UNLESS STRUCTURE CHANGES !
#

example_entry_iltasanomat = {'id': 2000010488185, 'href': '/musiikki/art-2000010488185.html', 'displayDate': '2024-06-10T13:31:00.000+03:00', 'title': 'Archie Cruz täräytti julki mielipiteensä Metallican keikasta – sitten huippu\xadartistit saapuivat kommentti\xadkenttään', 'picture': {'id': 2000010488416, 'width': 1920, 'height': 1080, 'url': 'https://is.mediadelivery.fi/img/WIDTH/eb8ad29be8784035d7eb4c348201e768.jpg', 'squareUrl': 'https://is.mediadelivery.fi/img/square/WIDTH/eb8ad29be8784035d7eb4c348201e768.jpg'}, 'ingress': 'Muun muassa Maija Vilkkumaa on vastannut Archie Cruzin kommenttiin.', 'paidType': 'free', 'category': 'Musiikki', 'infoRowEnabled': True}
example_entry_iltalehti = {}
example_entry_hs = {}
example_entry_yle = {}

#
# ---------------------------------------
#

def test_fetch():
    iltasanomat = Iltasanomat()
    articles = iltasanomat.fetch()
    assert len(articles) > 0
    assert articles[0].get("id")

def test_get_articles_fetch_timeout(monkeypatch):
    iltasanomat = Iltasanomat()
    def mock_fetch(self):
        raise TimeoutError("TimeoutError")
    monkeypatch.setattr("src.implementations.iltasanomat.Iltasanomat.fetch", mock_fetch)
    articles = iltasanomat.get_articles()
    assert articles == []

def test_get_articles_fetch_value_error(monkeypatch):
    iltasanomat = Iltasanomat()
    def mock_fetch(self):
        raise ValueError("ValueError")
    monkeypatch.setattr("src.implementations.iltasanomat.Iltasanomat.fetch", mock_fetch)
    articles = iltasanomat.get_articles()
    assert articles == []

def test_parser():
    iltasanomat = Iltasanomat()
    parsed = iltasanomat.parse(example_entry_iltasanomat)
    assert all([
        parsed.title == example_entry_iltasanomat["title"],
        parsed.time == datetime.strptime(example_entry_iltasanomat["displayDate"], "%Y-%m-%dT%H:%M:%S.%f%z")
    ])

def test_get_articles_parser_fail(monkeypatch):
    iltasanomat = Iltasanomat()
    def mock_fetch(self):
        return [("test", 0)]
    monkeypatch.setattr("src.implementations.iltasanomat.Iltasanomat.fetch", mock_fetch)
    articles = iltasanomat.get_articles()
    assert articles == []

def test_success():
    iltasanomat = Iltasanomat()
    articles = iltasanomat.get_articles()
    assert type(articles[0]) == APIResponse