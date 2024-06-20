import requests
from typing import List
from ..abstractions.resthandler import RestHandler
from ..abstractions.apiresponse import APIResponse
from ..endpoints import ILTASANOMAT
from datetime import datetime

class Iltasanomat(RestHandler):
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
        r = requests.get(ILTASANOMAT, timeout=10)
        return r.json()
    
    def parse(self, entry) -> APIResponse:
        source = "IS"
        id = entry["id"]
        title = entry["title"].replace("\xad", "")
        time_str = entry["displayDate"]
        time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        time = time.replace(tzinfo=None)
        return APIResponse(id, source, title, time)