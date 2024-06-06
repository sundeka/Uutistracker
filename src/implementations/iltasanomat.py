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
            r = requests.get(ILTASANOMAT, timeout=10)
        except TimeoutError:
            self.logger.error("Request timed out!")
            return articles
        try:
            data = r.json()
            for entry in data:
                parsed = self.parse(entry)
                articles.append(parsed)
        except ValueError:
            self.logger.error("Unable to parse JSON data!")
        return articles

    def parse(self, entry) -> APIResponse:
        source = "Ilta-Sanomat"
        title = entry["title"]
        time_str = entry["displayDate"]
        time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        return APIResponse(source, title, time)