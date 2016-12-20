#!/usr/bin/python
# encoding: utf-8
#
# Copyright (c) 2016 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2016-03-13
#

"""Wiktionary variants."""

from __future__ import print_function, absolute_import

from collections import namedtuple
import json

from bs4 import BeautifulSoup as BS

from common import datapath, httpget, log, mkdata, mksearch

url = 'https://www.wiktionary.org'
path = datapath('Wiktionary.html')

SEARCH_URL = 'https://{w.lang}.wiktionary.org/wiki/{{query}}'
SUGGEST_URL = 'https://{w.lang}.wiktionary.org/w/api.php?action=opensearch&search={{query}}'

Wiki = namedtuple('Wiki', 'id url lang name')


def html():
    return httpget(url, path)


def main():

    soup = BS(html(), 'html.parser')
    # Use 'langlist-large' css class for wiktionaries with
    # 10K+ entries.
    # Class 'langlist' will get wikitionaries with 100+ entries.
    data = mkdata('wiktionary', 'Wiktionary', 'Collaborative dictionary')
    # data = {
    #     'uid': 'wiktionary',
    #     'title': 'Wiktionary',
    #     'description': 'Collaborative dictionary',
    #     'searches': [],
    # }
    for div in soup.find_all('div', class_='langlist-large'):
        for link in div.select('ul li a'):
            log('link=%r', link)
            lang = id_ = link['lang']
            url = 'https:' + link['href']
            name = link.get_text()
            latin = link.get('title')
            if latin:
                name = u'{} / {}'.format(name, latin)
            w = Wiki(id_, url, lang, name)
            log('%r', w)
            url = SEARCH_URL.format(w=w)
            uid = u'wiktionary.{}'.format(w.lang)
            d = mksearch(uid, w.name,
                         u'Wiktionary ({w.name})'.format(w=w),
                         url, SUGGEST_URL.format(w=w),
                         u'wiktionary.png', w.lang)
            data['searches'].append(d)
            # data['searches'].append({
            #     'uid': uid,
            #     'title': w.name,
            #     'description': u'Wiktionary ({w.name})'.format(w=w),
            #     'search_url': url,
            #     'suggest_url': SUGGEST_URL.format(w=w),
            #     'icon': u'wiktionary.png',
            #     'lang': w.lang,
            #     'country': u'',
            # })

    print(json.dumps(data, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
