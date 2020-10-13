import TableRead as HI


def ExtractDate(url):
    soup = HI.soupinit(url)
    content = soup.find("div", attrs={"class": "body pod_gameinfo_left"}).find("ul")
    li = content.find_all("li")
    date = li[4].find("a", href=True)
    return date


def ExtractTable(page_num):
    page = genpage + str(page_num)
    soup = HI.soupinit(page)
    table = soup.find().find("table", attrs={'class': 'results'}).find("tbody")
    for tr in table.find_all('tr'):
        td = tr.find_all("td")
        system, game, rank = td[1:4]
        name = HI.undiv(game)
        game = home + HI.exhref(game)  # now a URL to game's own page
        name = name.replace(',', '.').replace('\u016b', 'u').replace('\u00e9', 'e').replace('\xe4', 'a')
        # '\u016b'='ū' '\u00e9'='é' '\xe4'='ä'
        date = ExtractDate(game)
        line = [HI.undiv(cel) for cel in (name, system, rank, date)]
        line = ",".join(line)
        line = line.replace('&amp;', '&')
        report.write(line + '\n')


if __name__ == '__main__':
    home = "https://gamefaqs.gamespot.com"
    report = open(' GameFAQs.csv', 'w+')
    platform = ''
    genpage = home + "/games/rankings&min_votes=2?platform=" + platform + '?page='
    Rank = 5
    page_num = 1
    report.write('Name,System,rating,date')
    while Rank >= 3.7:
        print('\npage:', page_num)
        ExtractTable(page_num)
        page_num += 1
