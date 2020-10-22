import TableRead as HI


def ExtractDate(url):
    soup = HI.soupinit(url)
    content = soup.find("div", attrs={"class": "body pod_gameinfo_left"})
    if not content:
        content = soup.find("div", attrs={"class": "pod pod_gameinfo"})
    if not content:
        print("no idea where right table is", url)
    content = content.ul
    li = content.find_all("li")

    for pl in li:
        b = HI.undiv(pl.find('b'))
        if b[:3] == "Rel":  # "Release:"
            date = pl.find("a", href=True)
            break
    try:
        date
    except NameError:
        print("unknown date:", url)
        return "Unknown"

    date = HI.undiv(date)
    date = date.split(' ')
    ln = len(date)
    if ln > 2:
        date = [date[1], date[0], date[2]]
    elif ln == 1:
        if not date[0] in {'TBA', 'Canceled'}:  # we actually only looking for a year
            date = ['december', date[0]]
    else:
        if date[0][0] == 'Q':  # the first charecter of the first word is Q, a quarter rather than day.
            quart = int(date[0][1])  # the second charecter is the number of the quarter
            month = 3 * quart
            date = [int(month), date[1]]
    date = "/".join(date).replace(',', '')
    return date


def ExtractTable(page_num):
    global rank
    page = genpage + str(page_num)
    print('\npage:', page, rank)
    soup = HI.soupinit(page)
    table = soup.find("div", attrs={'class': 'main_content row'}).table.tbody
    for tr in table.find_all('tr'):
        td = tr.find_all("td")
        system, game, rank = td[1:4]
        name   = HI.undiv(game)
        system = HI.undiv(system)
        rank   = HI.undiv(rank)  # effective end point for side-effect
        game   = home + HI.exhref(game)  # now a URL to game's own page
        name = name.replace(',', '.').replace('ū', 'u').replace('é', 'e').replace('ä', 'a')
        # '\u016b'='ū' '\u00e9'='é' '\xe4'='ä. é appears particularly in all them pokémon games.
        date = ExtractDate(game)
        line = ",".join([name, system, rank, date])
        line = line.replace('&amp;', '&')
        report.write(line + '\n')


if __name__ == '__main__':
    home = "https://gamefaqs.gamespot.com"
    report = open('try.csv', 'w+')
    genpage = home + "/games/rankings?min_votes=2&dlc=1" + '&page='
    rank = 5
    page_num = 0
    report.write('Name,System,rating,date\n')
    while rank >= 3.7:
        ExtractTable(page_num)
        page_num += 1
        rank = float(rank)
