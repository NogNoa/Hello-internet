import os

import requests

from TableRead import *

root_adress = "https://web.archive.org/web/20060106073452/http://www.cs.vu.nl/pub/amoeba/"


def save_as(local_path, file_type=""):
    resp = requests.get(root_adress + local_path)
    if not file_type:
        if resp.text.startswith("<!DOCTYPE HTML"):
            local_path += ".html"
        with open(local_path, "w+", encoding=resp.apparent_encoding) as codex:
            codex.write(resp.text)
    else:
        with open(local_path, "wb+") as codex:
            codex.write(bytes(resp.text, encoding="ascii"))


def extract_directory(local_path):
    url = root_adress + local_path
    soup = soup_init(url=url)
    try:
        os.mkdir(local_path)
    except FileExistsError: pass
    for tag in soup.body:
        tag.extract()
        if tag.string == " END WAYBACK TOOLBAR INSERT ":
            break
    for img in soup.body.find_all("img"):
        link = img.next.next["href"]
        if not link:
            print(f'url="{url}", element="{img.next}"')
            continue
        suffix = img["src"].split("/")[-1]
        if suffix == "unknown.gif":
            save_as(local_path + link)
        elif suffix == "folder.gif":
            extract_directory(local_path + link)
        elif suffix == "compressed.gif":
            save_as(local_path + link, "archive")
        else:
            print(suffix)


if __name__ == "__main__":
    os.chdir(r"G:\Source\sites\Amoeba")
    extract_directory("amoeba5.3/")
