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

    def __str__(self) -> str:
        """(<time>) <AGENCY NAME>: <headline>"""
        return f"({str(self.time.hour).zfill(2)}:{str(self.time.minute).zfill(2)}) {(self.source.upper())}: {self.title}"
    
    def __eq__(self, other):
        """Use ID for checking equality between APIResponse objects.
        Headlines may change, but the id attribute should remain the same.
        Most robust way to avoid duplicates."""
        return self.id == other.id