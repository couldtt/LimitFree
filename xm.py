__author__ = 'couldtt'
import threading
import pymongo
from config import config, crawl_container, DEBUG, debug_container
from bottle import route, run, jinja2_view


def get_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.books
    return db

class Crawl(threading.Thread):

    def __init__(self, type):
        crawler_name = type.capitalize() + "Crawler"
        crawler_module = __import__('LimitFreeCrawler')
        crawler_concrete = getattr(crawler_module, crawler_name)
        self.crawler = crawler_concrete(config[type])

    def run(self):
        try:
            res = self.crawler.start()
        except:
            res = []
        return res


if DEBUG:
    crawl_container = debug_container


@route('/')
@jinja2_view('index.html', template_lookup=['views'])
def index():
    platforms = []
    for site in crawl_container:
        crawl = Crawl(site)
        platforms.append(crawl.run())
    print(platforms)
    return {'platforms': platforms}


run(host='localhost', port=8080)