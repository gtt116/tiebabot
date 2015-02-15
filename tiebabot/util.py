import datetime


def now():
    n = datetime.datetime.now()
    return n.strftime('%Y-%m-%d %H:%M:%S')
