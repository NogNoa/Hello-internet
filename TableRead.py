import os
import random
from time import sleep

from aiohttp import ClientSession
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


async def gethtml(url, delay=1):
    sleep(delay + random.random() * 2)
    async with ClientSession() as session:
        scroll = await session.request(method="GET", url=url)
    html = await scroll.text()
    return html


async def soupinit(url=None):
    html = await gethtml(url)
    """ready BeutifulSoup when loading a new page"""
    soup = BeautifulSoup(html, features="html.parser")
    if not soup.head or soup.head.title == "502 Bad Gateway" or \
        not soup.body or soup.body.find("pre") in {"Gateway Timeout", "I/O error"}:
        errors.write(url + "\n\n")
        html = await gethtml(url, 27)
        soup = BeautifulSoup(html, features="html.parser")
    print(f'page: {url}')
    return soup


def clean():
    errors.close()
