from src.implementations.iltasanomat import Iltasanomat
from src.implementations.stt import Stt
from src.implementations.iltalehti import Iltalehti
from src.abstractions.apiresponse import APIResponse
from datetime import datetime

#
# DON'T MODIFY UNLESS STRUCTURE CHANGES !
#

example_entry_iltasanomat = {'id': 2000010488185, 'href': '/musiikki/art-2000010488185.html', 'displayDate': '2024-06-10T13:31:00.000+03:00', 'title': 'Archie Cruz täräytti julki mielipiteensä Metallican keikasta – sitten huippu\xadartistit saapuivat kommentti\xadkenttään', 'picture': {'id': 2000010488416, 'width': 1920, 'height': 1080, 'url': 'https://is.mediadelivery.fi/img/WIDTH/eb8ad29be8784035d7eb4c348201e768.jpg', 'squareUrl': 'https://is.mediadelivery.fi/img/square/WIDTH/eb8ad29be8784035d7eb4c348201e768.jpg'}, 'ingress': 'Muun muassa Maija Vilkkumaa on vastannut Archie Cruzin kommenttiin.', 'paidType': 'free', 'category': 'Musiikki', 'infoRowEnabled': True}
example_entry_stt = {"headline":"Thaimaassa noin tuhat lemmikkieläintä kuoli tulipalossa turistien suosimalla torilla","docdate":"2024-06-11T09:53:52.000+03:00","lookalikes":[{"url":"https://www.aamulehti.fi/ulkomaat/art-2000010491328.html","source_name":"Aamulehti"},{"url":"https://www.aamuposti.fi/uutissuomalainen/6835898","source_name":"Aamuposti"},{"url":"https://www.ess.fi/uutissuomalainen/6835898","source_name":"Etelä-Suomen Sanomat"},{"url":"https://www.forssanlehti.fi/uutissuomalainen/6835898","source_name":"Forssan Lehti"},{"url":"https://www.hs.fi/maailma/art-2000010491310.html","source_name":"Helsingin Sanomat"},{"url":"https://www.is.fi/kotimaa/art-2000010491274.html","source_name":"Ilta-Sanomat"},{"url":"https://www.itahame.fi/uutissuomalainen/6835898","source_name":"Itä-Häme"},{"url":"https://www.ita-savo.fi/uutissuomalainen/6835898","source_name":"Itä-Savo"},{"url":"https://www.keski-uusimaa.fi/uutissuomalainen/6835898","source_name":"Keski-Uusimaa"},{"url":"https://www.lansi-uusimaa.fi/uutissuomalainen/6835898","source_name":"Länsi-Uusimaa"},{"url":"https://www.mtvuutiset.fi/artikkeli/noin-tuhat-lemmikkielainta-kuoli-tulipalossa-thaimaassa/8955874","source_name":"MTV Uutiset"},{"url":"https://www.savonsanomat.fi/uutissuomalainen/6835898","source_name":"Savon Sanomat"},{"url":"https://www.warkaudenlehti.fi/uutissuomalainen/6835898","source_name":"Warkauden Lehti"}]}
example_entry_iltalehti = {"article_id":"6162de74-f845-47df-adc7-a09a0fa6a977","lead":"Välimeren dieettiä on hehkutettu jo pitkään. Nyt uusi tutkimustieto kertoo, että se sopii erityisen hyvin naisille. Suurtutkimuksen osallistujia seurattiin peräti 25 vuoden ajan. ","headline":"Nainen: Syö näin ","title":"Nainen: Syö näin ","keywords":["24h","Ruoka","Ruoka ja juoma","Ravitsemus","Terveys","Ravintoaine"],"functional_keywords":["author_edith_andersson"],"updated_at":None,"service_name":"iltalehti","main_image_name":"10040a464fbb681a386a111b2b2cb219e1719a0b2d1415c4cc62a809b6e68f2b.jpg","metadata":{"longform":False,"alma_source":"","article_type":None,"hide_all_ads":False,"newspilot_id":"","canonical_url":None,"some_vignette":None,"author_location":"","sponsored_content":None,"recommendations_enabled":True},"subscription_level":None,"category":{"category_name":"ravinto","description":"Ravinto","is_commercial":False,"sidecolumns":[],"parent_category":{"category_name":"hyvaolo","description":"Hyvä olo","is_commercial":False,"sidecolumns":[],"parent_category":None}},"main_image_urls":{"default":""},"published_at":"2024-06-11T11:03:34+03:00"}
example_entry_hs = {}

#
# ---------------------------------------
#

def test_fetch():
    iltasanomat = Iltasanomat()
    articles = iltasanomat.fetch()
    assert len(articles) > 0
    assert articles[0].get("id")

    stt = Stt()
    articles = stt.fetch()
    assert len(articles) > 0
    assert articles[0].get("headline")

    iltalehti = Iltalehti()
    articles = iltalehti.fetch()
    assert articles[0].get("article_id")

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

    stt = Stt()
    parsed = stt.parse(example_entry_stt)
    assert parsed.id > 999999

    iltalehti = Iltalehti()
    parsed = iltalehti.parse(example_entry_iltalehti)
    assert parsed.id == example_entry_iltalehti["article_id"]

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