from gamecube import undiv, exhref
from selenium import webdriver
from bs4 import BeautifulSoup


def gethtml(url):
    driver.get(url)
    return driver.page_source


def soupinit(url):
    """ready BeutifulSoup when loading a new page"""
    html = gethtml(url)
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def ExtractTable(startpage):
    """extracts the information of all games from the table"""
    global cond
    page = gentable + "&startpage=" + str(startpage)
    soup = soupinit(page)
    content = soup.find("body").find("div", attrs={"id": "wrapper"}).find("div", attrs={"id": "main"})
    # try:
    # abort = content.find("div", attrs={"class": "newsitem"}).find("div", attrs={"class": "newsbody"})
    # abort = undiv(abort)
    # if abort[:24] == "INVALID STARTPAGE VALUE"
    try:
        table = content.find("table").find("tbody")
    except:
        cond = False
        return
    for tr in table.find_all('tr'):
        hacks = tr.find("td", attrs={'class': hackname}).find("a", href=True)
        hkpg = home + exhref(hacks)
        if hacks and CheckLang(hkpg):
            title = tr.find("td", attrs={'class': "col_1 Title"}).find("a", href=True)
            date = tr.find("td", attrs={'class': "col_4 Date"})
            genre = tr.find("td", attrs={'class': "col_5 Genre"})
            platform = tr.find("td", attrs={'class': "col_6 Platform"})
            gmpg = home + exhref(title)
            line = [undiv(td) for td in (title, gmpg, date, genre, platform, hkpg)]
            # title
            line[0] = line[0].replace(',', '.').replace('\u016b', 'u').replace('\u00e9', 'e')  # \u016b=ū \u00e9=é
            # genre
            line[3] = line[3].replace('&gt;', '>')
            line = ",".join(line)
            line = line.replace('&amp;', '&')
            report.write(line + '\n')


def CheckLang(hkpg):
    soup = soupinit(hkpg)
    languges = soup.findall('td', attrs={'class': "col_8 Lang"})
    languges = [undiv(lang) for lang in languges]
    return 'EN' in languges


if __name__ == '__main__':
    report = open('romtranslations.csv', 'w+')
    report.write('title,game page,date,genre,platform,translations page,\n')

    driver = webdriver.Firefox()

    home = "http://www.romhacking.net"
    gentable = home + "/?page=games&perpage=200&order=Date"

    cond = True
    hackname = "col_9 Trans"
    startpage = 1
    while cond:
        ExtractTable(startpage)
        startpage += 1
    report.write(report.read().replace('&amp;', '&').replace('&gt;', '>'))
