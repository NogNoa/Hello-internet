import TableRead as HI


def ExtractDate(url):
    soup = HI.soupinit(url)
    content = soup.find("div", attrs={"class": "body pod_gameinfo_left"})
    if not content:
        content = soup.find("div", attrs={"class": "pod pod_gameinfo"})
    if not content:
        print("no idea where right table is", url)
    content = content.find("ul")
    li = content.find_all("li")

    for pl in li:
        b = HI.undiv(pl.find('b'))
        if b[:3] == "Rel":  # "Release:"
            date = pl.find("a", href=True)
            continue
    try:
        date
    except NameError:
        print("unknown date:", url)
        return "Unknown"

    date = HI.undiv(date)
    date = date.split(' ')
    if len(date) > 2:
        date = date[1] + date[0] + date[2]
    date = "".join(date).replace(',', '')
    return date


def ExtractTable(page_num):
    global rank
    page = genpage + str(page_num)
    print('\npage:', page)
    soup = HI.soupinit(page)
    table = soup.find().find("table", attrs={'class': 'results'}).find("tbody")
    for tr in table.find_all('tr'):
        td = tr.find_all("td")
        system, game, rank = td[1:4]
        name, system, rank = HI.undiv((game, system, rank))
        game = home + HI.exhref(game)  # now a URL to game's own page
        name = name.replace(',', '.').replace('\u016b', 'u').replace('\u00e9', 'e').replace('\xe4', 'a')
        # '\u016b'='ū' '\u00e9'='é' '\xe4'='ä'
        date = ExtractDate(game)
        line = ",".join([name, system, rank, date])
        line = line.replace('&amp;', '&')
        report.write(line + '\n')


if __name__ == '__main__':
    home = "https://gamefaqs.gamespot.com"
    report = open('GameFAQs.csv', 'w+')
    genpage = home + "/games/rankings?min_votes=2&dlc=1" + '&page='
    rank = 5
    page_num = 0
    report.write('Name,System,rating,date,')
    while rank >= 3.7:
        ExtractTable(page_num)
        page_num += 1
        rank = float(rank)
