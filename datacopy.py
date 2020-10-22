# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:59:43 2020

@author: Omer
"""

from selenium import webdriver
from bs4 import BeautifulSoup

table = open('table.txt', 'w+')


class datacopy():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://gamefaqs.gamespot.com/games/rankings?platform=99&genre=0&list_type=rate&min_votes=2")

    def copy(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        table.write(element.get_attribute('innerHTML'))

    def extract(self):
        content = self.driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        tabel = soup.find("table", attrs={'class': 'results'})
        names=[]
        ratings=[]
        for tr in tabel.findAll('tr'):
            name = tr.find('a', href=True)
            names.append(str(name))
            print('name', name)
            for rating in tr.findAll('td', attrs={'class': 'remain'}):
                ratings.append((rating + '\t'))
                print('rating', rating)


dat = datacopy()
dat.copy("/html/body/div[2]/div[4]/div[2]/div/div/header/h1")
dat.extract()
