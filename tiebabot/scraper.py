import requests
import logging
from bs4 import BeautifulSoup

LOG = logging.getLogger(__name__)


class Tieba(object):

    url = 'http://tieba.baidu.com/f?kw=%(name)s&ie=utf-8&pn=%(page)s'

    def __init__(self, name):
        self.name = name

    def read_page(self, page_number):
        """Returns the unicode of html content."""
        url = self.page_url(page_number)
        while True:
            try:
                resp = requests.get(url, timeout=3)
            except Exception as ex:
                LOG.warn("Read %s failed: %s, retry." % (url, ex))
                continue
            return resp.text

    def page_url(self, page_number):
        page = (int(page_number) - 1) * 50
        if page < 0:
            page = 0

        return self.url % {'page': page, 'name': self.name}


class TiebaModel(object):
    root_url = 'http://tieba.baidu.com'

    def __init__(self, reply_number, title, last_replier, author, link):
        self.reply_number = int(reply_number)
        self.title = title.strip()
        self.last_replier = last_replier.strip()
        self.author = author.strip()
        self._link = link.strip()

        self.raw_html = None

    @property
    def link(self):
        return self.root_url + '/' + self._link + "?see_lz=1"

    @property
    def id(self):
        return self._link.split('/')[-1]

    def __repr__(self):
        return "<Item %s>" % self.title.encode('utf8')


class Parser(object):

    def parse(self, content, encoding=None):
        soup = BeautifulSoup(content, from_encoding=encoding)
        items = soup.select("li.j_thread_list.clearfix")

        resp = []
        for item in items:
            resp.append(self._parse_item(item))
        return resp

    def _parse_item(self, item):
        try:
            reply_number = item.find('div', class_='threadlist_rep_num').text
        except AttributeError:
            reply_number = '0'

        try:
            title = item.find('div', class_='threadlist_title').text
        except AttributeError:
            title = ''

        try:
            author = item.find('div', class_='threadlist_author').text
        except AttributeError:
            author = ''

        try:
            replier = item.find('span', class_='j_replyer').text
        except AttributeError:
            replier = ''

        try:
            link = item.find('a')['href']
        except TypeError:
            link = ''

        real_item = TiebaModel(reply_number, title, author, replier, link)
        real_item.raw_html = unicode(item)
        return real_item


class Sorder(object):

    @staticmethod
    def sort(items):
        return sorted(items, key=lambda x: x.title, reverse=True)


class IdSorder(object):

    @staticmethod
    def sort(items):
        return sorted(items, key=lambda x: x.id, reverse=True)
