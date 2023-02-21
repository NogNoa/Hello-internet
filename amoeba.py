import os

import requests

from TableRead import *

root_adress = "https://web.archive.org/web/20060106073452/http://www.cs.vu.nl/pub/amoeba/"

os.chdir(r"G:\Source\sites\Amoeba")


def save_as(local_path, file_type=""):
    resp = requests.get(root_adress + local_path)
    if not file_type:
        with open(local_path, "w+", encoding=resp.apparent_encoding) as codex:
            codex.write(resp.text)
    else:
        with open(local_path, "wb+") as codex:
            codex.write(bytes(resp.text))
        if file_type != "archive":
            print(file_type)


def extract_directory(local_path):
    url = root_adress + local_path
    soup = soup_init(url=url)
    os.mkdir(local_path)
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
            save_as(local_path + link)
        elif img["src"].endswith("folder.gif"):
            extract_directory(local_path + link)
        elif img["src"].endswith("compressed.gif"):
            save_as(local_path + link, "archive")


if __name__ == "__main__":
    extract_directory("amoeba5.3")
