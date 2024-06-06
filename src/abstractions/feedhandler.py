from typing import List
from .apiresponse import APIResponse
import logging

class FeedHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    def get_articles() -> List[APIResponse]: pass
    def parse() -> APIResponse: pass