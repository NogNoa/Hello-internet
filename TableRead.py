from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Firefox()


def undiv(txt):
    """removes the formating from an html line and leaves the internal string"""
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
    """takes the url part of a hyperlink"""
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


def gethtml(url):
    global driver
    driver.get(url)
    return driver.page_source


def soupinit(url):
    """ready BeutifulSoup when loading a new page"""
    html = gethtml(url)
    soup = BeautifulSoup(html, features="html.parser")
    return soup


