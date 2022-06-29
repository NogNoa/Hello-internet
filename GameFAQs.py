import TableRead as HI


def extract_date(html, name):
    soup = HI.soupinit(html=html)
    content = soup.body.find("div", attrs={"class": "body pod_gameinfo_left"})
    if not content:
        content = soup.body.find("div", attrs={"class": "pod pod_gameinfo"})
    if not content:
        print("no idea where right table is", html)
        with open("errors.log", 'a+', encoding="utf-8") as errors:
            errors.write("extract_date: No right table found:" + name + "\n" + html + "\n\n")
        return "Unknown"
    content = content.ol if content.ol else content.ul
    lii = content.find_all("li")
    for li in lii:
        b = HI.undiv(li.find('b'))
        if b.startswith("Release"):
            date = li.find("a", href=True)
            break

    if "date" not in locals():
        with open("errors.log", 'a+', encoding="utf-8") as errors:
            errors.write("No Date Found:" + html)
        return "Unknown"

    date = HI.undiv(date)
    date = date.split(' ')
    date = [i for i in date if i != '']
    ln = len(date)
    if ln > 2:
        date = [date[1], date[0], date[2]]
    elif ln == 1:
        if not date[0] in {'TBA', 'Canceled'}:  # we actually only looking for a year
            date = ['december', date[0]]
    else:
        if date[0][0] == 'Q':  # the first character of the first word is Q, a quarter rather than day.
            quart = int(date[0][1])  # the second character is the number of the quarter
            month = 3 * quart
            date = [str(month), date[1]]
    date = "/".join(date).replace(',', '')
    return date


def extract_wankers(html, name):
    # wankers in actually rankers, it's a joke gimeabreak
    soup = HI.soupinit(html=html)
    rate_text = soup.find("div", attrs={"id": "gs_rate_avg_hint", "class": "gamespace_rate_hint"})
    rate_text = HI.undiv(rate_text)
    wankers = ''
    for char in rate_text:
        if char in '0123456789':
            wankers += char
    if wankers == '':
        with open("errors.log", 'a+', encoding="utf-8") as errors:
            errors.write("No Wankers: " + name + "\n")
        return '0'
    return wankers


def extract_genres(html, name):
    soup = HI.soupinit(html=html)
    content = soup.body.find("div", attrs={"class": "body pod_gameinfo_left"})
    if not content:
        content = soup.body.find("div", attrs={"class": "pod pod_gameinfo"})
    if not content:
        print("no idea where right table is", html)
        with open("errors.log", 'a+', encoding="utf-8") as errors:
            errors.write("extract_genres:No right table found:" + name + "\n" + html + "\n\n")
        return ["Unknown"]
    content = content.ol if content.ol else content.ul
    lii = content.find_all("li")
    for li in lii:
        b = HI.undiv(li.find('b'))
        if b.startswith("Genre"):
            genri = li
            break

    if "genri" not in locals():
        with open("errors.log", 'a+', encoding="utf-8") as errors:
            errors.write("No Genres Found:" + name + "\n" + html + "\n\n")
        return ["Unknown"]

    genri = genri.find_all("a", href=True)
    genri = [HI.undiv(genre).lower() for genre in genri]
    return genri


def extract_table(page_num, row_num, book_nom, cutoff_wankers=0, genre_ignore=()):
    global rank
    page = genpage + str(page_num)
    print('\npage:', page, rank)
    soup = HI.soupinit(url=page)
    table = soup.find("div", attrs={'class': 'main_content row'}).table.tbody
    tri = table.find_all('tr')
    for i, tr in enumerate(tri[row_num:]):
        save.write((page_num, row_num+i))
        td = tr.find_all("td")
        game = td[1].a
        name = HI.undiv(game)
        system = HI.undiv(td[1].span)
        rank = HI.undiv(td[2])  # effective end point for side effect
        game = home + HI.exhref(game)  # now a URL to game's own page
        name = name.replace(',', '.').replace('ū', 'u').replace('é', 'e').replace('ä', 'a')
        # '\u016b'='ū' '\u00e9'='é' '\xe4'='ä. é appears particularly in all them pokémon games.
        game_html = HI.gethtml(game)
        wankers = extract_wankers(game_html, name)
        if int(wankers) < cutoff_wankers:
            continue
        genri = extract_genres(game_html, name)
        if set(genre_ignore).intersection(genri):
            continue
        date = extract_date(game_html, name)
        line = ",".join([name, system, rank, wankers, date])
        line = line.replace('&amp;', '&')
        with open(book_nom, 'a', encoding="utf-8") as report:
            report.write(line + '\n')
        print(line)



if __name__ == '__main__':
    import begin_resume

    home = "https://gamefaqs.gamespot.com"
    genpage = home + "/games/rankings?min_votes=2&dlc=1&page="
    save = begin_resume.Save("gamefaq.sav")
    cutoff_rank = 3.7
    rank = 5
    book_nom ="GameFAQs4.csv"
    try:
        page_num, row_num = save.read()
    except begin_resume.SaveNotFoundError:
        page_num = row_num = 0
        with open(book_nom, 'w+', encoding="utf-8") as report:
            report.write('Name,System,rating,rankers,date\n')
    while rank >= cutoff_rank:
        extract_table(page_num, row_num, book_nom, cutoff_wankers=25, genre_ignore=("sports",))
        page_num += 1
        row_num = 0
        save.write((page_num, row_num))
        rank = float(rank)
    HI.clean()

