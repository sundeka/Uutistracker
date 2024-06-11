from datetime import datetime

class APIResponse:
    def __init__(self, id: int, source: str, title: str, time: datetime):
        self.id = id
        self.source = source
        self.title = title
        self.time = time

    def __str__(self) -> str:
        return f"({str(self.time.hour).zfill(2)}:{str(self.time.minute).zfill(2)}) {(self.source.upper())}: {self.title}"
    
    def __eq__(self, other):
        return self.id == other.id