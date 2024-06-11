import requests
from typing import List
from ..abstractions.feedhandler import FeedHandler
from ..abstractions.apiresponse import APIResponse
from ..endpoints import ILTASANOMAT
from datetime import datetime

class Iltasanomat(FeedHandler):
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
        title = entry["title"]
        time_str = entry["displayDate"]
        time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        return APIResponse(id, source, title, time)