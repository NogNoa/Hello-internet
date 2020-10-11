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
        hacks = tr.find("td", attrs={'class': "col_10 Hacks"}).find("a", href=True)
        hkpg = home + exhref(hacks)
        if hacks:  # and CheckLang(hkpg):
            title = tr.find("td", attrs={'class': "col_1 Title"}).find("a", href=True)
            date = tr.find("td", attrs={'class': "col_4 Date"})
            genre = tr.find("td", attrs={'class': "col_5 Genre"})
            platform = tr.find("td", attrs={'class': "col_6 Platform"})
            gmpg = home + exhref(title)
            title = undiv(title)
            title = title.replace('&amp;', '&')
            try:
                report.write(title)
            except:
                title = title.replace('\u016b', 'u').replace('\u00e9', 'e') # \u016b=ū \u00e9=é
                report.write(title)
                print(title+)
            line = ','
            for td in (gmpg, date, genre, platform, hkpg):
                td = undiv(td)
                line += td + ', '
            line = line.replace('&amp;', '&').replace('&gt;', '>')
            report.write(line + '\n')


def CheckLang(hkpg):
    soup = soupinit(hkpg)
    languges = soup.findall('td', attrs={'class': "col_8 Lang"})
    for lang in languges:
        lang = undiv(lang)
    return ('EN' in languges)


if __name__ == '__main__':
    report = open('romhacking.csv', 'w+')
    report.write('title,game page,date,genre,platform,translations page,\n')

    driver = webdriver.Firefox()

    home = "http://www.romhacking.net"
    gentable = home + "/?page=games&perpage=200&order=Date"

    cond = True
    startpage = 1
    while cond:
        ExtractTable(startpage)
        startpage += 1
    report.write(report.read().replace('&amp;', '&').replace('&gt;', '>'))
