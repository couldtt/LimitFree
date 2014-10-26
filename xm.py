__author__ = 'couldtt'
import threading
from config import config, crawl_container, DEBUG, debug_container

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
            res = {}
        return res


if DEBUG:
    crawl_container = debug_container

for site in crawl_container:
    crawl = Crawl(site)
    print(crawl.run())