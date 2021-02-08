import TableRead as HI


def ExtractDate(html):
    soup = HI.soupinit(html)
    content = soup.find("div", attrs={"class": "body pod_gameinfo_left"})
    if not content:
        content = soup.find("div", attrs={"class": "pod pod_gameinfo"})
    if not content:
        print("no idea where right table is", html)
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
        print("unknown date:", html)
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


def ExtractWankers(html,name):
    # wankers in actually rankers, it's a joke gimeabreak
    soup = HI.soupinit(html)
    rate_text = soup.find("div", attrs={"id": "gs_rate_avg_hint", "class": "gamespace_rate_hint"})
    if rate_text is None:
        open("nowankers.txt", "w+").write(name + "\n")
        return '0'
    rate_text = HI.undiv(rate_text)
    wankers = ''
    for char in rate_text:
        if char in '0123456789':
            wankers += char
    return wankers


def ExtractTable(page_num, cutoff_wankers=0):
    global rank
    page = genpage + str(page_num)
    print('\npage:', page, rank)
    soup = HI.soupinit(html=HI.gethtml(page))
    table = soup.find("div", attrs={'class': 'main_content row'}).table.tbody
    for tr in table.find_all('tr'):
        td = tr.find_all("td")
        system, game, rank = td[1:4]
        name = HI.undiv(game)
        system = HI.undiv(system)
        rank = HI.undiv(rank)  # effective end point for side-effect
        game = home + HI.exhref(game)  # now a URL to game's own page
        name = name.replace(',', '.').replace('ū', 'u').replace('é', 'e').replace('ä', 'a')
        # '\u016b'='ū' '\u00e9'='é' '\xe4'='ä. é appears particularly in all them pokémon games.
        game_html = HI.gethtml(game)
        wankers = ExtractWankers(game_html, name)
        if int(wankers) < cutoff_wankers:
            continue
        date = ExtractDate(game_html)
        line = ",".join([name, system, rank, wankers, date])
        line = line.replace('&amp;', '&')
        report.write(line + '\n')
        print(line)


if __name__ == '__main__':
    home = "https://gamefaqs.gamespot.com"
    report = open('GameFAQs3.csv', 'w+')
    genpage = home + "/games/rankings?min_votes=2&dlc=1" + '&page='
    cutoff_rank = 3.7
    rank = 5
    page_num = 0
    report.write('Name,System,rating,rankers,date\n')
    while rank >= cutoff_rank:
        ExtractTable(page_num, cutoff_wankers=15)
        page_num += 1
        rank = float(rank)
