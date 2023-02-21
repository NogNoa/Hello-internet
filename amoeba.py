import os

import requests

from TableRead import *

root_adress = "https://web.archive.org/web/20060106073452/http://www.cs.vu.nl/pub/amoeba/amoeba5.3/"

os.chdir(r"G:\Source\sites\Amoeba")


def save_as(name, inter, file_type=""):
    resp = requests.get(root_adress + inter + name)
    if not file_type:
        with open(inter + name, "w+", encoding=resp.apparent_encoding) as codex:
            codex.write(resp.text)
    else:
        with open(inter + name, "wb+") as codex:
            codex.write(bytes(resp.text))
        if file_type != "archive":
            print(file_type)


def extract_directory(base_dir, inter=""):
    inter += base_dir
    url = root_adress + inter
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
            save_as(link, inter)
        elif img["src"].endswith("folder.gif"):
            extract_directory(link, inter)
        elif img["src"].endswith("compressed.gif"):
            save_as(link, inter, "archive")
