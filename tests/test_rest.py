from src.implementations.iltasanomat import Iltasanomat
from src.implementations.stt import Stt
from src.implementations.iltalehti import Iltalehti
from src.abstractions.apiresponse import APIResponse
from datetime import datetime

EXAMPLE_STT = {"headline":"Thaimaassa noin tuhat lemmikkieläintä kuoli tulipalossa turistien suosimalla torilla","docdate":"2024-06-11T09:53:52.000+03:00","lookalikes":[{"url":"https://www.aamulehti.fi/ulkomaat/art-2000010491328.html","source_name":"Aamulehti"},{"url":"https://www.aamuposti.fi/uutissuomalainen/6835898","source_name":"Aamuposti"},{"url":"https://www.ess.fi/uutissuomalainen/6835898","source_name":"Etelä-Suomen Sanomat"},{"url":"https://www.forssanlehti.fi/uutissuomalainen/6835898","source_name":"Forssan Lehti"},{"url":"https://www.hs.fi/maailma/art-2000010491310.html","source_name":"Helsingin Sanomat"},{"url":"https://www.is.fi/kotimaa/art-2000010491274.html","source_name":"Ilta-Sanomat"},{"url":"https://www.itahame.fi/uutissuomalainen/6835898","source_name":"Itä-Häme"},{"url":"https://www.ita-savo.fi/uutissuomalainen/6835898","source_name":"Itä-Savo"},{"url":"https://www.keski-uusimaa.fi/uutissuomalainen/6835898","source_name":"Keski-Uusimaa"},{"url":"https://www.lansi-uusimaa.fi/uutissuomalainen/6835898","source_name":"Länsi-Uusimaa"},{"url":"https://www.mtvuutiset.fi/artikkeli/noin-tuhat-lemmikkielainta-kuoli-tulipalossa-thaimaassa/8955874","source_name":"MTV Uutiset"},{"url":"https://www.savonsanomat.fi/uutissuomalainen/6835898","source_name":"Savon Sanomat"},{"url":"https://www.warkaudenlehti.fi/uutissuomalainen/6835898","source_name":"Warkauden Lehti"}]}
EXAMPLE_IS = {'id': 2000010488185, 'href': '/musiikki/art-2000010488185.html', 'displayDate': '2024-06-10T13:31:00.000+03:00', 'title': 'Archie Cruz täräytti julki mielipiteensä Metallican keikasta – sitten huippu\xadartistit saapuivat kommentti\xadkenttään', 'picture': {'id': 2000010488416, 'width': 1920, 'height': 1080, 'url': 'https://is.mediadelivery.fi/img/WIDTH/eb8ad29be8784035d7eb4c348201e768.jpg', 'squareUrl': 'https://is.mediadelivery.fi/img/square/WIDTH/eb8ad29be8784035d7eb4c348201e768.jpg'}, 'ingress': 'Muun muassa Maija Vilkkumaa on vastannut Archie Cruzin kommenttiin.', 'paidType': 'free', 'category': 'Musiikki', 'infoRowEnabled': True}
EXAMPLE_IL = {"article_id":"6162de74-f845-47df-adc7-a09a0fa6a977","lead":"Välimeren dieettiä on hehkutettu jo pitkään. Nyt uusi tutkimustieto kertoo, että se sopii erityisen hyvin naisille. Suurtutkimuksen osallistujia seurattiin peräti 25 vuoden ajan. ","headline":"Nainen: Syö näin ","title":"Nainen: Syö näin ","keywords":["24h","Ruoka","Ruoka ja juoma","Ravitsemus","Terveys","Ravintoaine"],"functional_keywords":["author_edith_andersson"],"updated_at":None,"service_name":"iltalehti","main_image_name":"10040a464fbb681a386a111b2b2cb219e1719a0b2d1415c4cc62a809b6e68f2b.jpg","metadata":{"longform":False,"alma_source":"","article_type":None,"hide_all_ads":False,"newspilot_id":"","canonical_url":None,"some_vignette":None,"author_location":"","sponsored_content":None,"recommendations_enabled":True},"subscription_level":None,"category":{"category_name":"ravinto","description":"Ravinto","is_commercial":False,"sidecolumns":[],"parent_category":{"category_name":"hyvaolo","description":"Hyvä olo","is_commercial":False,"sidecolumns":[],"parent_category":None}},"main_image_urls":{"default":""},"published_at":"2024-06-11T11:03:34+03:00"}

def test_get_articles(monkeypatch):
    def mock_fetch_stt(self):
        return [EXAMPLE_STT]
    def mock_fetch_is(self):
        return [EXAMPLE_IS]
    def mock_fetch_il(self):
        return [EXAMPLE_IL]
    monkeypatch.setattr("src.implementations.stt.Stt.fetch", mock_fetch_stt)
    monkeypatch.setattr("src.implementations.iltasanomat.Iltasanomat.fetch", mock_fetch_is)
    monkeypatch.setattr("src.implementations.iltalehti.Iltalehti.fetch", mock_fetch_il)
    stt = Stt()
    iss = Iltasanomat()
    il = Iltalehti()
    for platform in (stt, iss, il):
        articles = platform.get_articles()
        assert len(articles) == 1
        assert type(articles[0]) == APIResponse
    
def test_parse():
    expected_stt = APIResponse(
        1718088832,
        "STT",
        "Thaimaassa noin tuhat lemmikkieläintä kuoli tulipalossa turistien suosimalla torilla",
        datetime(2024, 6, 11, 9, 53, 52)
    )
    expected_is = APIResponse(
        2000010488185,
        "IS",
        "Archie Cruz täräytti julki mielipiteensä Metallican keikasta – sitten huippuartistit saapuivat kommenttikenttään",
        datetime(2024, 6, 10, 13, 31, 00)
    )
    expected_il = APIResponse(
        "6162de74-f845-47df-adc7-a09a0fa6a977",
        "IL",
        "Nainen: Syö näin ",
        datetime(2024, 6, 11, 11, 3, 34)
    )
    stt = Stt()
    iss = Iltasanomat()
    il = Iltalehti()
    for platform, expected, raw in ((stt, expected_stt, EXAMPLE_STT), (iss, expected_is, EXAMPLE_IS), (il, expected_il, EXAMPLE_IL)):
        parsed = platform.parse(raw)
        assert all([
            parsed.id == expected.id,
            parsed.source == expected.source,
            parsed.title == expected.title,
            parsed.time == expected.time
        ])