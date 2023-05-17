import random
from time import sleep

import logging

logging.basicConfig(filename="errors_HI.log", encoding="utf-8")


class BadUrlError(ConnectionError):
    pass


def undiv(txt):
    """Removes the formating from an HTML line and leaves the internal string"""
    txt = str(txt)
    new = ''
    div = True
    for i in txt:
        if i == '<':
            div = False
        elif div:
            new += i
        elif i == '>':
            div = True
    return new


def exhref(txt):
    """Takes the url part of a hyperlink"""
    txt = str(txt)
    new = ''
    href = False
    j = 0
    for i in txt:
        if txt[j - 6:j] == 'href="':
            href = True
        elif txt[j:j + 2] == '">':
            href = False
        if href:
            new += i
        j += 1
    return new


def get_html(url, delay=1):
    import requests
    sleep(delay + random.random() * 2)
    scroll = requests.get(url)
    return scroll.text


def soup_init(url=None, html=None):
    from bs4 import BeautifulSoup
    if html is None:
        html = get_html(url)
    """ready BeutifulSoup when loading a new page"""
    soup = BeautifulSoup(html, features="html.parser")
    if not soup.head or soup.head.title == "502 Bad Gateway" or \
           not soup.body or soup.body.find("pre") in {"Gateway Timeout", "I/O error"}:
        print(url)
        logging.error(url + "\n")
        html = get_html(url, 27)
        soup = BeautifulSoup(html, features="html.parser")
    if soup.head and soup.head.title == "Not Found":
        raise BadUrlError
    return soup
