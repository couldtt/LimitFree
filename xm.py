__author__ = 'couldtt'
import threading
from config import crawl_config, crawl_container, DEBUG, debug_container, remark_config
from bottle import route, run, jinja2_view
from storage import MongoStorage

class Crawl(threading.Thread):

    def __init__(self, type):
        crawler_name = type.capitalize() + "Crawler"
        crawler_module = __import__('LimitFreeCrawler')
        crawler_concrete = getattr(crawler_module, crawler_name)
        self.crawler = crawler_concrete(crawl_config[type])

    def run(self):
        try:
            res = self.crawler.start()
        except:
            res = {}
        return res

if DEBUG:
    crawl_container = debug_container


@route('/')
@jinja2_view('index.html', template_lookup=['views'])
def index():
    ms = MongoStorage()
    try:
        record = ms.get_today()
        platforms = record['platforms']
    except:
        platforms = []
        for site in crawl_container:
            crawl = Crawl(site)
            platforms.append(crawl.run())
        ms.save(platforms)
    return {
        'platforms': platforms,
        'remarks': remark_config
    }

run(host='localhost', port=8080)