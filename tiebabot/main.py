# -*-coding:utf8-*-
import os
import logging

import scraper
import render
import util
import filters


TARGET_DIR = '/var/www/tieba/'
LOG = logging.getLogger(__name__)


class Scraper(object):
    def __init__(self, names, target_dir, template_name, max_page=3):
        self.names = names
        self.target_dir = target_dir
        self.template_name = template_name
        self.max_page = max_page

        self._parser = scraper.Parser()
        #TODO: make sure self.name existed

    def process(self):
        for name in self.names:
            threads = self._process(name)
            self.dump_to_file(threads, name)

    def _process(self, name):
        LOG.debug("Start processing: %s" % name)
        all_threads = []
        tieba = scraper.Tieba(name)
        for no in xrange(1, self.max_page + 1):
            LOG.debug("Start read page: %s" % no)
            page_content = tieba.read_page(no)
            rest = self._parser.parse(page_content, 'utf8')
            all_threads.extend(rest)

        sorted_threads = self.sort(all_threads)
        sorted_threads = self.filter(sorted_threads)
        return sorted_threads

    def filter(self, threads):
        LOG.debug("Filtering threads.")
        return filters.WaijiaoFilter().filter(threads)

    def sort(self, threads):
        LOG.debug("Sorting threads.")
        return scraper.Sorder.sort(threads)

    def dump_to_file(self, threads, name):
        LOG.debug("Dump to files.")
        now = util.now_unicode()
        target = os.path.join(self.target_dir, '%s.html' % name)
        render.render_to_file(self.template_name, target,
                              threads=threads, title=name,
                              updated_at=now, links=self.names)


if __name__ == '__main__':
    logging.basicConfig()
    LOG.setLevel(logging.DEBUG)
    titles = [u'apink', u'郑恩智', u'supergirls', u'2pm组合']
    Scraper(titles, TARGET_DIR, 'base_v1.html').process()
