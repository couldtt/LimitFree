__author__ = 'couldtt'
import threading
from config import config

class Crawl(threading.Thread):

    def __init__(self, type):
        crawler_name = type.capitalize() + "Crawler"
        crawler_module = __import__('LimitFreeCrawler')
        crawler_concrete = getattr(crawler_module, crawler_name)
        self.crawler = crawler_concrete(config[type]['url'])

    def run(self):
        try:
            res = self.crawler.start()
        except:
            res = {}
        return res

crawl_container = ['duokan', 'taobao']
for site in crawl_container:
    crawl = Crawl(site)
    print(crawl.run())