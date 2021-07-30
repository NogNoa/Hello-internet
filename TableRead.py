import selenium.common
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.minimize_window()
errors = open("errors_HI.log", 'w+', encoding="utf-8")


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


def re_gethtml(url, i, html):
    print(url)
    errors.write(url + "\n\n")
    refresh()
    sleep(30)
    if i < 12:  # 6 minutes
        return gethtml(url, i+1)
    else:
        return html


def gethtml(url, i=0):
    global driver
    try:
        driver.get(url)
        html = driver.page_source
    except selenium.common.exceptions.TimeoutException or selenium.common.exceptions.WebDriverException:
        html = re_gethtml(url, i, driver.page_source)
    soup = BeautifulSoup(html, features="html.parser")
    if soup.head.title == "502 Bad Gateway" or soup.body.pre in {"Gateway Timeout", "I/O error"}:
        html = re_gethtml(url, i, html)
    return html


def soupinit(url=None, html=None):
    if html is None:
        html = gethtml(url)
    """ready BeutifulSoup when loading a new page"""
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def clean():
    driver.close()
    errors.close()


def refresh():
    global driver
    driver.close()
    sleep(.5)
    driver = webdriver.Firefox()
    driver.minimize_window()
