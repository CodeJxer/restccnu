# coding: utf-8

import re
import base64
import requests
from bs4 import BeautifulSoup
from urlparse import urlsplit, parse_qs


def search_books(keyword):
    search_url = "http://202.114.34.15/opac/openlink.php"
    post_data = {
            'strSearchType': 'title',
            'match_flag': 'forward',
            'historyCount': '1',
            'strText': keyword,
            'doctype': 'ALL',
            'displaypg': '100',  # tomorrow
            'showmode': 'list',
            'sort': 'CATA_DATE',
            'orderby': 'desc',
            'dept': 'ALL'
    }
    r = requests.get(search_url, post_data)
    # r.encoding = 'utf-8'
    # soup = BeautifulSoup(r.content, 'lxml', from_encoding='iso-8859-1')
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    book_list_info = soup.find_all('li', class_='book_list_info')
    book_info_list = []
    for book_info in book_list_info:
        if book_info:
            bid_lit = book_info.h3.text.split()
            try:
                int(bid_lit[-1])
            except ValueError as e:
                bid = bid_lit[-1]
            else:
                bid = ' '.join(bid_lit[-2:])
            book = book_info.find('a', href=re.compile('item.php*')).string
            marc_no_link = book_info.find('a').get('href')
            marc_no = marc_no_link.split('=')[-1]
            # isbn_link =
            # isbn = isbn_link.split('=')
            book_info_list.append({
                'book': book,
                'author': ' '.join(book_info.p.text.split()[2:-4]),
                'bid': bid,
                'intro': 'intro',  # no intro ?
                'id': marc_no
            })
    return book_info_list


# http://202.114.34.15/opac/item.php?marc_no=0001364670G
def get_book(id, bid, book, author):
    """
    meet problem :(
    """
    detail_url = "http://202.114.34.15/opac/item.php?marc_no=%s" % id
    r = requests.get(detail_url)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')

    bid = bid; book = book; author = author
    intro = soup.find(id="fullsum") or ""
    # booklist: ['status', 'room', 'date', 'tid']
    booklist = []
    _booklist = soup.find(id='tab_item').find_all('tr', class_="whitetext")
    for _book in _booklist:
        lit = _book.text.split()
        if '-' in lit[-1]:
            date = lit[-1][-10:]
            status = lit[-1][:2]
            booklist.append({
                "status": status,
                "room": lit[-2],
                "bid": lit[0],
                "tid": lit[1],
                "date": date })
        else:
            booklist.append({
                "status": lit[-1],
                "room": lit[-2],
                "bid": lit[0],
                "tid": lit[1]})
    return {
        'bid': bid,
        'book': book,
        'author': author,
        'intro': intro,
        'books': booklist
    }
