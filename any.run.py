import sys

import selenium as sl
import bs4
import TableRead as TR


def extract_table(html):
    soup = TR.soupinit(html=html)
    table = soup.find("div", attrs={'class': "history-table--content"})
    rows = table.find_all('div')
    for row in rows:
        page = extract_mal(home + row.a["href"])


def extract_mal(url):
    soup = TR.soupinit(url=url)
    page = soup.find("a", attrs={"class": "reports__btn","id": "textReport"})
    return page

if __name__ == '__main__':
    import begin_resume

    home = "https://app.any.run"
    genpage = home + "/submissions"
    save = begin_resume.Save("anyrun.sav")
    book_nom = sys.argv[1]
    tag = sys.argv[2]
    try:
        page_num = save.read()
    except begin_resume.SaveNotFoundError:
        page_num = row_num = 0
        with open(book_nom, 'w+', encoding="utf-8") as report:
            report.write('<header text>')
    driver = sl.webdriver.Chrome()
    driver.get(genpage)
    driver.find_element({By.TAG_NAME: "i", By.CLASS_NAME: "fa fa-filter"}).click()
    tag_loc = driver.find_element({By.TAG_NAME: "input",By.ID: "hashtagSearch"})
    tag_loc.send_keys(tag)
    tag_loc.send_keys(Keys.RETURN)
    next_loc = driver.find_element({By.TAG_NAME: "button",
         By.CLASS_NAME: "history-pagination__next history-pagination__button history-pagination__element"})
    while True:
        extract_table(driver.page_source)
        next_loc.click()

