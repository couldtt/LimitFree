__author__ = 'couldtt'
import threading
import json
from config import crawl_config, crawl_container, debug_container, remark_config
from bottle import route, run, jinja2_view
from storage import MongoStorage


DEBUG = False
WEB_DEBUG = False

class Crawl(threading.Thread):

    def __init__(self, type):
        crawler_name = type.capitalize() + "Crawler"
        crawler_module = __import__('LimitFreeCrawler')
        crawler_concrete = getattr(crawler_module, crawler_name)
        self.crawler = crawler_concrete(crawl_config[type])

    def run(self):
        if DEBUG:
            self.crawler.start()
        else:
            try:
                res = self.crawler.start()
            except:
                res = []
            return res

if DEBUG:
    for site in debug_container:
        crawl = Crawl(site)
        crawl.run()

@route('/')
@jinja2_view('index.html', template_lookup=['views'])
def index():
    return {
        'platforms': crawl_container,
        'remarks': remark_config
    }


@route('/p/<site>')
def get_book(site):
    ms = MongoStorage()
    if site in crawl_container:
        record = ms.get_today(site)
        if record and WEB_DEBUG == False:
            platform = record['platform']
        else:
            crawl = Crawl(site)
            platform = crawl.run()
            ms.save(site, platform)
        return platform

@route('/platforms')
def get_platforms():
    return json.dumps(crawl_container)

def main():
    run(server='gunicorn', host='localhost', port=8080)

if __name__ == '__main__':
    main()