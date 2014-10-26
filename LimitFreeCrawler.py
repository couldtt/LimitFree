__author__ = 'couldtt'
# encoding=utf-8
import urllib3
import re
from abc import abstractmethod

class Crawler():

    http = urllib3.PoolManager()

    def __init__(self, url):
        self.base_url = url
        self.res = {}
        r = self.http.request('GET', url)
        self.charset = r.headers['Content-Type'].split('=')[1]
        self.page_content = r.data.decode(self.charset)

    def pre_parse(self):
        pass

    @abstractmethod
    def pipe(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    def start(self):
        self.pre_parse()
        self.parse()
        self.pipe()
        return self.res

# 淘宝
class TaobaoCrawler(Crawler):

    def parse(self):
        pattern = re.compile(r".*limit_item\['(.+?)'\] = '(.+?)';")
        self.matches = pattern.findall(self.page_content)

    def pipe(self):
        for match in self.matches:
            if (match[0] == 'src'):
                self.res['img'] = match[1]
            else:
                self.res[match[0]] = match[1]

# 多看
class DuokanCrawler(Crawler):

    def pre_parse(self):
        pattern = re.compile(r'<li><a href\s?="(.+?)".*alt="限时免费"')
        self.matches = pattern.findall(self.page_content)
        url = self.matches[0]
        self.res['href'] = self.base_url + url
        r = self.http.request('GET', "http://" + self.res['href'])
        self.page_content = r.data.decode(self.charset)

    def parse(self):
        pattern = re.compile(r'<img itemprop="image" src="(?P<src>.+?)" alt="(.+?)".*>')
        self.matches = pattern.findall(self.page_content)

    def pipe(self):
        self.res['img'] = self.matches[0][0]
        self.res['title'] = self.matches[0][1]