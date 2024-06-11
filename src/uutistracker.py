from src.implementations.iltasanomat import Iltasanomat
from src.implementations.stt import Stt
from src.implementations.iltalehti import Iltalehti
from typing import List
from src.abstractions.apiresponse import APIResponse
import time
import itertools
from colorama import Fore

class Uutistracker:
    def __init__(self):
        self.iltasanomat = Iltasanomat()
        self.stt = Stt()
        self.iltalehti = Iltalehti()

    def start(self):
        previous_headlines = []
        while True:
            queue = self.generate_queue()
            sorted_queue = self.sort_queue(queue)
            chopped_queue = self.chop_queue(sorted_queue)
            new_headlines = self.check_new_headlines(chopped_queue, previous_headlines)
            self.print(new_headlines)
            previous_headlines = chopped_queue
            self.wait()

    def generate_queue(self) -> List[APIResponse]:
        """Forms an unsorted queue from all news outlets."""
        q = []
        for outlet in [self.iltasanomat, self.stt, self.iltalehti]:
            articles = outlet.get_articles()
            q.extend(articles)
        return q

    def sort_queue(self, q: List[APIResponse]):
        """Sorts the queue so that the oldest article is always at index 0."""
        for idx in range(1, len(q)):
            curr = q[idx]
            j = idx-1
            while j>=0 and q[j].time > curr.time:
                q[j+1] = q[j]
                j-=1
            q[j+1] = curr
        return q
    
    def chop_queue(self, q: List[APIResponse]):
        """Chop the queue so that it only contains 10 headlines at most."""
        length = len(q)
        if length>=10:
            return q[(length-10):length]
        return q # Should never really get here
    
    def check_new_headlines(self, new: List[APIResponse], old: List[APIResponse]) -> List[APIResponse]:
        new_headlines = []
        for new_headline in new:
            if new_headline not in old:
                new_headlines.append(new_headline)
        return new_headlines

    def print(self, new_headlines: List[APIResponse]):
        """(<time>) <AGENCY NAME>: <headline>"""
        for headline in new_headlines:
            if "juuri nyt" in headline.title.lower():
                c = Fore.RED
                print(c + f"({str(headline.time.hour).zfill(2)}:{str(headline.time.minute).zfill(2)}) {(headline.source.upper())}: {headline.title}")
                c = Fore.RESET
            else:
                c = Fore.RESET
                print(c + f"({str(headline.time.hour).zfill(2)}:{str(headline.time.minute).zfill(2)})", end=" ")
                match headline.source:
                    case "Iltalehti":
                        c = Fore.LIGHTRED_EX
                    case "Ilta-Sanomat":
                        c = Fore.YELLOW
                    case "STT":
                        c = Fore.WHITE
                print(c + headline.source.upper(), end=" ")
                c = Fore.RESET
                print(c + headline.title)

    def wait(self):
        t = 100
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if t==0:
                break
            print(f"Waiting for new headlines... {c}", end="\r")
            time.sleep(0.5)
            t-=1