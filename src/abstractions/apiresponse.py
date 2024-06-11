from datetime import datetime

"""
A uniform structure that represents a single headline received from the API.
"""
class APIResponse:
    def __init__(self, id: int, source: str, title: str, time: datetime):
        self.id = id
        self.source = source
        self.title = title
        self.time = time
    
    def __eq__(self, other):
        """Use ID for checking equality between APIResponse objects.
        Headlines may change, but the id attribute should remain the same.
        Most robust way to avoid duplicates."""
        return self.id == other.id