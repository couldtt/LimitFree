__author__ = 'couldtt'
# encoding=utf-8
import re
from abc import abstractmethod
import urllib3
from bs4 import BeautifulSoup


class Crawler():

    http = urllib3.PoolManager()

    def __init__(self, config):
        self.config = config
        self.base_url = self.config['url']
        self.res = []  # 最终返回的今日免费电子书集合
        r = self.http.request('GET', self.config['url'])
        try:
            self.charset = r.headers['Content-Type'].split('=')[1]
        except:
            self.charset = 'gbk'
        self.page_content = r.data.decode(self.charset, 'ignore')  # 为了避免解析当当网的时候出现一些诡异的无法解码的错误

    def pre_parse(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def pipe(self):
        pass

    def save(self):
        pass

    def start(self):
        self.pre_parse()
        self.parse()
        self.pipe()
        platform = {
            'config': self.config,
            'books': self.res,
        }
        return platform

# 淘宝
class TaobaoCrawler(Crawler):

    def parse(self):
        pattern = re.compile(r".*limit_item\['(.+?)'\] = '(.+?)';")
        self.matches = pattern.findall(self.page_content)

    def pipe(self):
        res = {}
        for match in self.matches:
            if match[0] == 'src':
                res['img'] = match[1]
            else:
                res[match[0]] = match[1]
        self.res.append(res)

# 多看
class DuokanCrawler(Crawler):

    def pre_parse(self):
        pattern = re.compile(r'<li><a href\s?="(.+?)".*alt="限时免费"')
        self.matches = pattern.findall(self.page_content)
        url = self.matches[0]
        new_href = self.base_url + url
        r = self.http.request('GET', new_href)
        self.page_content = r.data.decode(self.charset)
        self.href = new_href

    def parse(self):
        pattern = re.compile(r'<img itemprop="image" src="(?P<src>.+?)" alt="(.+?)".*>')
        matches = pattern.findall(self.page_content)
        if matches:
            self.matches = matches
        else:
            pattern = re.compile(r'<a href="(.+?)".*><img src="(.+?)" alt="(.+?)" ondragstart="return false;" oncontextmenu="return false;".*></a>')
            matches = pattern.findall(self.page_content)
            self.matches = matches

    def pipe(self):
        if len(self.matches) > 1:
            for match in self.matches:
                res = {}
                res['img'] = match[1]
                res['title'] = match[2]
                res['href'] = self.config['url'] + match[0]
                self.res.append(res)
        else:
            res = {}
            res['img'] = self.matches[0]
            res['title'] = self.matches[1]
            res['href'] = self.href
            self.res.append(res)

# 当当
class DangdangCrawler(Crawler):
    def __init__(self, config):
        self.res = []
        self.config = config

    '''
    当当的特价专区是使用ajax加载的，所以需要先读取其ajax载入的html内容，然后对该html进行解析
    关于构造函数，似乎可以再网上进行一层抽象，剥离出ajax加载和非ajax加载的部分，重新进行继承
    重造两个抽象的爬虫NormalCrawler、AjaxCrawler
    '''

    def pre_parse(self):
        r = self.http.request('GET', self.config['ajax_url'])
        self.charset = r.headers['Content-Type'].split('=')[1]
        self.page_content = r.data.decode(self.charset, 'ignore')

    def parse(self):
        soup = BeautifulSoup(self.page_content)
        div_tab_1 = soup.find_all('ul', id='component_74284__1631_1629__1629')[0]
        self.matches = div_tab_1.find_all('a', class_='img')

    def pipe(self):
        for match in self.matches:
            res = {}
            res['href'] = match.get('href')
            res['title'] = match.get('title')
            res['img'] = match.find('img').get('src')
            self.res.append(res)


# 网易
class NeteaseCrawler(Crawler):
    def pre_parse(self):
        r = self.http.request('GET', self.config['ajax_url'])
        self.page_content = r.data.decode(self.charset, 'ignore')

    def parse(self):
        soup = BeautifulSoup(self.page_content)
        m_highlight = soup.find('div', class_='m-highlight')
        self.match = m_highlight

    def pipe(self):
        res = {}
        res['author'] = self.match.find('p', class_='author').contents[0].split(':')[1]
        j_cutted = self.match.find('a', class_='j-cutted')
        res['img'] = self.match.find('img').get('src')
        res['href'] = j_cutted.get('href')
        res['title'] = j_cutted.contents[0]
        self.res.append(res)


# 百度
class BaiduCrawler(Crawler):
    def pre_parse(self):
        soup = BeautifulSoup(self.page_content)
        cd_act_0 = soup.find('div', id='cd-act-0')
        self.new_href = cd_act_0.find('a', class_='act-link').get('href')
        r = self.http.request('GET', self.new_href)
        self.page_content = r.data.decode(self.charset, 'ignore')

    def parse(self):
        soup = BeautifulSoup(self.page_content)
        doc_info_bd = soup.find('div', class_='doc-info-bd')
        self.match = doc_info_bd

    def pipe(self):
        res = {}
        res['href'] = self.new_href
        res['img'] = self.match.find('img', class_='doc-info-img').get('src')
        res['title'] = self.match.find('h1', class_='book-title').get('title')
        res['author'] = self.match.find('a', class_='doc-info-author-link').contents[0]
        self.res.append(res)