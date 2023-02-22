import os
from sys import argv

import requests

from TableRead import *
from bs4 import BeautifulSoup

root_adress = "https://"


def save_as(local_path: str):
    if os.path.exists(local_path) and os.path.getsize(local_path):
        return
    sleep(random.random() * 10)
    resp = requests.get(root_adress + local_path)
    with open(local_path, "wb+") as codex:
        codex.write(resp.content)
    print(local_path)


def wayback_strip(soup: BeautifulSoup) -> BeautifulSoup:
    for tag in soup.head:
        tag.extract()
        if tag.string == " End Wayback Rewrite JS Include ":
            break
    bodies = soup.body.__iter__()
    for tag in bodies:
        if tag.string == " BEGIN WAYBACK TOOLBAR INSERT ":
            break
    for tag in bodies:
        tag.extract()
        if tag.string == " END WAYBACK TOOLBAR INSERT ":
            break
    return soup


def extract_directory(local_path: str, wayback=False):
    url = root_adress + local_path
    soup = soup_init(url=url)
    try:
        os.mkdir(local_path)
    except FileExistsError:
        pass
    if wayback:
        soup = wayback_strip(soup)
    for img in soup.body.find_all("img"):
        link = img.next.next["href"]
        if not link:
            print(f'url="{url}", element="{img.next}"')
            continue
        suffix = img["src"].split("/")[-1]
        if suffix in {"unknown.gif", "compressed.gif", "tar.gif"}:
            save_as(local_path + link)
        elif suffix == "folder.gif":
            extract_directory(local_path + link)
        elif suffix in {"blank.gif", "back.gif"}:
            pass
        else:
            print(suffix)


def extract_site(local_path: str, wayback=False):
    url = root_adress + local_path
    soup: BeautifulSoup = soup_init(url=url)
    try:
        if local_path:
            os.mkdir(local_path)
    except FileExistsError:
        pass
    print(local_path)
    if wayback:
        soup = wayback_strip(soup)
    codex_nom = url.split("/")[-2] + ".html"
    with open(local_path + codex_nom, "w+", encoding="utf-8") as codex:
        codex.write(soup.text)
    for tag in soup.head:
        if tag.has_attr("href"):
            link = tag["href"]
            if link.startswith("http") :
                if link.startswith(url):
                    link = link.lstrip(url)
                save_as(local_path + link)
            elif link.startswith("#"):
                continue
            else:
                extract_site(local_path + link)
        if tag.has_attr("src"):
            save_as(local_path + tag["src"])


if __name__ == "__main__":
    root_adress = argv[1]
    os.chdir(argv[2])
    extract_site(argv[3])
