import os

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
        os.mkdir(local_path)
    except FileExistsError:
        pass
    if wayback:
        soup = wayback_strip(soup)
    with open(local_path, "w+") as codex:
        codex.write(soup.text)
    for tag in soup.head:
        if tag.has_attr("href"):
            link = tag["href"]
            if link.startswith("http") and not link.startswith(root_adress):
                save_as(local_path + link)
            elif link.startswith("#"):
                continue
            else:
                extract_site(local_path + link)
        if tag.has_attr("src"):
            save_as(local_path + tag["src"])


if __name__ == "__main__":
    root_adress = "https://web.archive.org/web/20060106073452/http://www.cs.vu.nl/pub/amoeba/"
    os.chdir(r"G:\Source\sites\Amoeba")
    extract_directory("amoeba5.3/")
