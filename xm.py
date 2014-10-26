__author__ = 'couldtt'
from LimitFreeCrawler import TaobaoCrawler, DuokanCrawler
import threading

class Crawl(threading.Thread):

    def __init__(self, type):
        if type == 'taobao':
            self.url = "ebook.taobao.com"
            self.crawler = TaobaoCrawler(self.url)
        elif type == 'duokan':
            self.url = "www.duokan.com"
            self.crawler = DuokanCrawler(self.url)

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