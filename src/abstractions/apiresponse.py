from datetime import datetime

class APIResponse:
    def __init__(self, source: str, title: str, time: datetime):
        self.source = source
        self.title = title
        self.time = time

    def __str__(self) -> str:
        return f"{(self.source.upper())} ({self.time.hour}:{self.time.minute}): {self.title}"
    
    def __eq__(self, other):
        return self.title == other.title