import os
import random
from time import sleep

import requests
from bs4 import BeautifulSoup

errors = open("errors_HI.log", 'w+', encoding="utf-8")


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


async def re_gethtml(url, html):
    print(url)
    errors.write(url + "\n\n")
    sleep(30)
    scroll = os.popen(f"wsl curl {url}")
    return scroll.read()


"""except selenium.common.exceptions.TimeoutException or selenium.common.exceptions.WebDriverException:
        return html"""


async def gethtml(url):
    sleep(random.random() * 5)
    scroll = os.popen(f"wsl curl \"{url}\"")
    html = scroll.read()
    soup = BeautifulSoup(html, features="html.parser")
    if not soup.head or soup.head.title == "502 Bad Gateway" or \
        not soup.body or soup.body.find("pre") in {"Gateway Timeout", "I/O error"}:
        html = await re_gethtml(url, html)
    print(f'page: {url}')
    return html


async def soupinit(url=None):
    html = await gethtml(url)
    """ready BeutifulSoup when loading a new page"""
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def clean():
    errors.close()
