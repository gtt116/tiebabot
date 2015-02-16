#-*-coding:utf8-*-
import re


class Filter(object):

    @staticmethod
    def filter(items):
        raise NotImplementedError()


class WaijiaoFilter(Filter):

    @staticmethod
    def filter(items):
        re_pattern = ur'.*外交.*'
        pattern = re.compile(re_pattern, re.UNICODE)

        new_items = []
        for item in items:
            if re.match(pattern, item.title) is None:
                new_items.append(item)
        return new_items
