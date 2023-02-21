from TableRead import *


def save_as(url, type=""):
    pass


def extract_directory(url):
    soup = soup_init(url=url)
    for tag in soup.body:
        tag.extract()
        if tag.string == " END WAYBACK TOOLBAR INSERT ":
            break
    for img in soup.body.find_all("img"):
        link = img.next["href"]
        if not link:
            print(f'url="{url}", element="{img.next}"')
            continue
        if img["src"].endswith("unknown.gif"):
            save_as(link)
        elif img["src"].endswith("folder.gif"):
            extract_directory(link)
        elif img["src"].endswith("compressed.gif"):
            save_as(link, "archive")

