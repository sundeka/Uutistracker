from src.implementations.iltasanomat import Iltasanomat
from typing import List
from src.abstractions.apiresponse import APIResponse
import time

class Uutistracker:
    def __init__(self):
        self.iltasanomat = Iltasanomat()
        self.feed_previous: List[APIResponse] = []
        self.feed_current: List[APIResponse] = []

    def start(self):
        while True:
            self.update_feed()
            new_headlines = self.check_new_headlines()
            if new_headlines:
                new_headlines = self.sort(new_headlines)
            self.sort(self.feed_current)
            try:
                self.feed_current = self.feed_current[:10]
            except IndexError:
                pass
            self.feed_previous = self.feed_current
            self.print(new_headlines)
            self.wait()

    def update_feed(self):
        for outlet in [self.iltasanomat]:
            articles = outlet.get_articles()
            self.feed_current.extend(articles)

    def check_new_headlines(self):
        if not self.feed_previous:
            return self.feed_current # First run, all headlines are new
        new_headlines = []
        old_headlines = [headline.title for headline in self.feed_previous]
        for headline in self.feed_current:
            if headline.title not in old_headlines:
                new_headlines.append(headline)
        return new_headlines
    
    def sort(self, arr: List[APIResponse]):
        for idx in range(1, len(arr)):
            curr = arr[idx]
            j = idx-1
            while j>=0 and arr[j].time < curr.time:
                arr[j+1] = arr[j]
                j-=1
            arr[j+1] = curr
        return arr

    def print(self, new_headlines: List[APIResponse] = None):
        if not new_headlines:
            for headline in self.feed_current:
                print(str(headline)+"\n")
        else:
            for headline in new_headlines:
                print(str(headline)+"\n")

    def wait(self):
        time.sleep(10)