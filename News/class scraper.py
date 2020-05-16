from bs4 import BeautifulSoup
from dotenv import load_dotenv
from secrets import password
import datetime
import redis
import requests


class Scraper:
    def __init__(self, keywords):
        self.markup = requests.get('https://news.ycombinator.com/').text
        self.keywords = keywords

    def parse(self):
        soup = BeautifulSoup(self.markup, 'html.parser')
        links = soup.findAll("a", {"class": "storylink"})
        self.saved_links = []
        for link in links:
            for keyword in self.keywords:
                if keyword in link.text:
                    self.saved_links.append(link)

    def store(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        for link in self.saved_links:
            r.set(link.text, str(link))

        
s = Scraper(['database'])
s.parse()
s.store()
if datetime.datetime.now().hour == 13:
    s.email()