import os
from sys import argv

import requests

from TableRead import *
from bs4 import BeautifulSoup

root_adress = "https://"


def save_as(name: str, inter: str, domain: str = root_adress):
    local_path = inter + name
    friendly_path = local_path.replace("?", "_")
    if os.path.exists(friendly_path) and os.path.getsize(friendly_path):
        print(local_path)
        return
    if domain != root_adress:
        try:
            os.makedirs(inter, )
        except FileExistsError:
            pass
    sleep(random.random() * 10)
    resp = requests.get(domain + local_path)
    with open(friendly_path, "wb+") as codex:
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
            save_as(link, local_path)
        elif suffix == "folder.gif":
            extract_directory(local_path + link)
        elif suffix in {"blank.gif", "back.gif"}:
            pass
        else:
            print(suffix)


def extract_tag(tag, local_path):
    try:
        for sub in tag.children:
            extract_tag(sub, local_path)
    except AttributeError:
        pass
    try:
        if tag.has_attr("href"):
            link = tag["href"]
        elif tag.has_attr("src"):
            link = tag["src"]
        else:
            return
    except AttributeError:
        return
    if link.startswith("http"):
        adrs = link.split("/")
        domain = "/".join(adrs[:3]) + "/"
        path = "/".join(adrs[3:-1]) + "/"
        name = adrs[-1]
        save_as(name, path, domain)
    elif link.startswith("#"):
        return
    else:
        if tag.has_attr("href"):
            extract_site(link, local_path)
        elif tag.has_attr("src"):
            save_as(link, local_path)

def extract_site(page: str, inter: str = "", wayback=False):
    local_path = inter + page
    url = root_adress + local_path
    soup: BeautifulSoup = soup_init(url=url)
    if local_path:
        codex_nom = local_path.split("/")[-2] + ".html"
    else:
        codex_nom = root_adress.split("/")[-2] + ".html"
    try:
        os.mkdir(".".join(codex_nom.split(".")[:-1]))
    except FileExistsError:
        if os.path.exists(local_path + codex_nom) and os.path.getsize(local_path + codex_nom):
            print(local_path + codex_nom)
            return
    if wayback:
        soup = wayback_strip(soup)
    for tag in soup:
        extract_tag(tag, local_path)
    with open(local_path + codex_nom, "w+", encoding="utf-8") as codex:
        codex.write(soup.text)
    print(local_path)


if __name__ == "__main__":
    root_adress = argv[1]
    os.chdir(argv[2])
    extract_site(argv[3])

# todo: travel children
