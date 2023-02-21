"""
A script for making a table games of score >3.6 out of 5 for a single platform based on gamefaqs's users
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from TableRead import undiv, exhref


class datacopy():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.home = "https://gamefaqs.gamespot.com"

    def soupinit(self):
        """ready BeutifulSoup when loading a new page"""
        content = self.driver.page_source
        self.soup = BeautifulSoup(content, features="html.parser")

    def ExtractGame(self):
        """extracts the information of each game"""
        self.soupinit()
        # zoom on the main content segment
        content = self.soup.find("div", attrs={'class': "main_content row"})
        # takes the name of the game
        name = content.find("h1", attrs={"class": "page-title"})
        name = undiv(name).replace("&amp;", "&") + ','
        # takes the rating o/ of 5 of the game
        # old field = "fieldset", "id": "js_mygames_rate"
        field = content.find("div", attrs={"class": "body gamespace_rate_box", })
        try:
            section = field.find("div", attrs={"class": "subsection-title"})
        except:
            # if we don't find rating, just warn and exit
            report.write(name + '\n')
            print("EMPTY GAME?")
            return
        rating = section.find("a", href=True)
        rating = undiv(rating)[:4]
        self.Rank = float(rating)  # passing the ranking to check later if we're above 3.6
        rating = rating + ","
        # takes the realese date of the game
        bodypod = content.find("div", attrs=({"class": "body pod_gameinfo_left"} or {"class": "pod pod_gameinfo"}))
        if bodypod is None:
            bodypod = content.find("aside", attrs={"class": "span4"})
        """li=bodypod.findAll("li")[3]    
        date = li.find("a", href=True)"""
        for li in bodypod.findAll("li"):
            b = li.find("b")
            if undiv(b) == "Release:":
                date = li.find("a", href=True)
                break
        date = undiv(date).replace(",", '')
        # we need to reorder the date if it's full, becuase 'murica
        datel = date.split()  # datel = date list
        if len(datel) > 2:
            date = datel[1] + ' ' + datel[0] + ' ' + datel[2]
        elif len(datel) == 1 and date != 'Canceled':
            date = "30/12/" + date
        date += ','
        # sends the information to a CSV file
        for noun in [name, rating, date]:
            print(noun)
            report.write(noun)
        report.write("\n")
        self.driver.get(self.page)
        self.soupinit()

    def LookTable(self):
        self.soupinit()
        table = self.soup.find("table", attrs={'class': 'results'})
        for tr in table.findAll('tr'):
            """if self.Rank < 3.6:
                break"""
            game = tr.find('a', href=True)
            if game != None:
                # get the href
                game = exhref(str(game))
                # print(game)
                self.driver.get(self.home + game)
                self.ExtractGame()

    def extractall(self, platform):
        self.page = self.home + "/games/rankings?platform=" + str(platform) + "&genre=0&list_type=rate&min_votes=2"
        page0 = self.page
        self.Rank = 5
        p = 1  # integer value for page
        while self.Rank >= 3.6:
            print('\npage:', p)
            self.driver.get(self.page)
            self.LookTable()
            self.page = page0 + "&page=" + str(p)
            p += 1


if __name__ == '__main__':
    report = open(' dual-screen.csv', 'w+')
    dat = datacopy()
    dat.extractall('108')

""" 99 = gamecube
    59 = gameboy 
    41 = nes
    84 = nintendo 64
    108 = DS
    """
