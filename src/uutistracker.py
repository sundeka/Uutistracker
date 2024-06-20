from src.implementations.iltasanomat import Iltasanomat
from src.implementations.stt import Stt
from src.implementations.iltalehti import Iltalehti
from src.implementations.hs import Helsinginsanomat
from src.implementations.yle import Yle
from typing import List
from src.abstractions.apiresponse import APIResponse
import time
import itertools
import sys
from colorama import Back
from datetime import datetime

class Uutistracker:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.iltasanomat = Iltasanomat()
        self.stt = Stt()
        self.iltalehti = Iltalehti()
        self.helsinginsanomat = Helsinginsanomat()
        self.yle = Yle()

    def start(self):
        previous_headlines = []
        while True:
            queue = self.generate_queue()
            sorted_queue = self.sort_queue(queue)
            chopped_queue = self.chop_queue(sorted_queue)
            new_headlines = self.check_new_headlines(chopped_queue, previous_headlines)
            self.print(new_headlines)
            previous_headlines.extend(new_headlines)
            self.wait()

    def generate_queue(self) -> List[APIResponse]:
        """Forms an unsorted queue from all news outlets."""
        q = []
        for outlet in [self.iltasanomat, self.stt, self.iltalehti, self.helsinginsanomat, self.yle]:
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
        if self.debug:
            for article in q:
                print(article.source + ": " + "(" + str(article.time) + ") " + article.title)
        return q
    
    def chop_queue(self, q: List[APIResponse]):
        """Chop the queue so that it only contains 10 headlines at most."""
        length = len(q)
        if length>=10:
            return q[(length-10):length]
        return q # Should never really get here
    
    def check_new_headlines(self, new: List[APIResponse], old: List[APIResponse]) -> List[APIResponse]:
        new_headlines = []
        old_headline_ids = [headline.id for headline in old]
        old_headline_titles = [headline.title for headline in old]
        for new_headline in new:
            if new_headline.id not in old_headline_ids:
                # If id is new -> new headline altogether
                new_headlines.append(new_headline)
            elif new_headline.title not in old_headline_titles:
                # Headline with same id exists, but title is updated -> treat as a new headline with updated timestamp
                new_headline.time = datetime.now()
                new_headlines.append(new_headline)
        return new_headlines

    def print(self, new_headlines: List[APIResponse]):
        """(<time>) <AGENCY NAME>: <headline>"""
        highlightables = ["IL:", "HS:", "IS:", "Yle:", "media:", "tiedetään nyt", "on kuollut"]
        for headline in new_headlines:
            if any(keyword in headline.title.lower() for keyword in highlightables):
                c = Back.RED
                print(c + f"({str(headline.time.hour).zfill(2)}:{str(headline.time.minute).zfill(2)}) {(headline.source)} {headline.title}")
                c = Back.RESET
            else:
                c = Back.RESET
                print(c + f"({str(headline.time.hour).zfill(2)}:{str(headline.time.minute).zfill(2)})", end=" ")
                match headline.source:
                    case "IL":
                        c = Back.LIGHTRED_EX
                    case "IS":
                        c = Back.YELLOW
                    case "STT":
                        c = Back.WHITE
                    case "HS":
                        c = Back.BLUE
                    case "YLE":
                        c = Back.MAGENTA
                print(c + headline.source, end="")
                c = Back.RESET
                print(c + " " + headline.title)

    def wait(self):
        t = 60
        for c in itertools.cycle(['.', '..', '...', '...', '....', '.....']):
            if t==0:
                break
            print(c, end="\r")
            sys.stdout.write("\033[K")
            time.sleep(0.5)
            t-=1