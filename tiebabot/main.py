import os

import scraper
import render
import util


TARGET_DIR = '/var/www/tieba/'

if __name__ == '__main__':
    parser = scraper.Parser()
    tieba = scraper.Tieba('apink')

    all_threads = []
    for no in xrange(1, 4):
        page_content = tieba.read_page(no)
        rest = parser.parse(page_content, 'utf8')
        all_threads.extend(rest)

    sorted_rest = scraper.Sorder.sort(all_threads)

    now = util.now()
    target = os.path.join(TARGET_DIR, 'apink.html')
    render.render_to_file('base.html', target,
                          threads=sorted_rest, title='Apink',
                          updated_at=now)
