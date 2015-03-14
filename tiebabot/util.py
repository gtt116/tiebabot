import datetime


def now():
    n = datetime.datetime.now()
    return n.strftime('%Y-%m-%d %H:%M:%S')


def now_unicode():
    return unicode(now())


def now_short():
    return datetime.datetime.now().strftime("%H:%M")
