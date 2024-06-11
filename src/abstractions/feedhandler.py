from typing import List
from .apiresponse import APIResponse
import logging

class FeedHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    def get_articles() -> List[APIResponse]:
        """The main driver function that handles all the exception handling.
        Calls fetch() and parse()."""
        pass
    def fetch() -> List[dict]:
        """Makes a request to the news agency's API endpoint and returns the response as a list of dicts."""
        pass
    def parse() -> APIResponse: 
        """Parses the individual REST entry and converts it into an APIResponse object."""
        pass