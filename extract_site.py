import os
from sys import argv

import requests

from TableRead import *
import bs4
import logging

root_scheme = "https://"
logging.basicConfig(filename="extract-site.log")


def path_build(codex_nom: str):
    folder_nom = ""
    for fldr in codex_nom.split("/")[:-1]:
        folder_nom += f"{fldr}/"
        print(f"folder: {folder_nom}")
        try:
            os.mkdir(folder_nom)
        except FileExistsError:
            if os.path.exists(codex_nom) and os.path.getsize(codex_nom):
                print(codex_nom)


def save_as(name: str, inter: str = '', scheme: str = root_scheme):
    if inter: inter = inter.rstrip("/") + "/"
    local_path = inter + name
    codex_nom = local_path
    if os.path.exists(codex_nom) and os.path.getsize(codex_nom):
        print(local_path)
        return
    if name.split("/")[:-1]:
        path_build(local_path)
    sleep(random.random() * 10)
    resp = requests.get(scheme + local_path)
    with open(codex_nom, "wb+") as codex:
        codex.write(resp.content)
    print(local_path)


def wayback_strip(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
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


def extract_tag(tag: bs4.element, local_path=''):
    try:
        for sub in tag.children:
            if isinstance(sub, bs4.Tag): extract_tag(sub, local_path)
        if tag.has_attr("href"):
            link = tag["href"]
            if tag.has_attr("rel") and tag["rel"][0] == "stylesheet":
                ext_func = save_as
            else:
                ext_func = extract_page
        elif tag.has_attr("src"):
            link = tag["src"]
            ext_func = save_as
        else:
            return
    except AttributeError:
        return
    link = link.partition("#")[0].partition("?")[0]
    if any((link in memory, local_path + link in memory, root_adress + link in memory)):
        return
    if link.startswith("http"):
        memory.add(link)
        adrs = link.split("/")
        domain = (adrs[2]) + "/"
        if domain == root_adress:
            scheme = "/".join(adrs[:2]) + "/"
            path = "/".join(adrs[3:-1]) + "/"
            name = adrs[-1]
            ext_func(name, domain + path, scheme=scheme)
        else:
            return
    elif link.startswith("/"):
        memory.add(root_adress + link)
        ext_func(link)
    else:
        memory.add(local_path + link)
        ext_func(link, local_path)


def extract_page(page: str, inter: str = '', wayback=False, **kwargs):
    if inter: inter = inter.rstrip('/') + '/'
    if page.endswith("/"):
        local_path = inter + page
        codex_nom = local_path.rstrip("/") + ".html"
        url = root_scheme + local_path
    elif page.endswith(".html"):
        local_path = inter
        codex_nom = inter + page
        url = root_scheme + codex_nom
        if url == root_adress + "index.html":
            return
    else:
        logging.error(f"page:{page}, inter:{inter}")
        return
    if page.split("/")[:-1]:
        path_build(local_path)
    soup: bs4.BeautifulSoup = soup_init(url=url)
    if soup.html: soup = soup.html
    if wayback:
        soup = wayback_strip(soup)
    for tag in soup:
        if isinstance(tag, bs4.Tag): extract_tag(tag, local_path)
    with open(codex_nom, "w+", encoding="utf-8") as codex:
        codex.write(str(soup))
    print(codex_nom)


def extract_site(wayback=False, **kwargs):
    codex_nom = root_adress + "index.html"
    path_build(codex_nom)
    soup: bs4.BeautifulSoup = soup_init(url=root_scheme + root_adress)
    if soup.html: soup = soup.html
    if wayback:
        soup = wayback_strip(soup)
    for tag in soup:
        if isinstance(tag, bs4.Tag): extract_tag(tag, root_adress)
    with open(codex_nom, "w+", encoding="utf-8") as codex:
        codex.write(str(soup))
    print(codex_nom)


if __name__ == "__main__":
    root_adress = argv[1]
    root_scheme, _, root_adress = root_adress.partition("://")
    if root_adress:
        root_scheme += "://"
    else:
        root_adress = root_scheme
        root_scheme = "http://"
    root_adress = root_adress.rstrip("/") + "/"
    memory = {root_adress, "/"}
    os.chdir(argv[2])
    if argv[3].startswith('dir'):
        extract_directory(argv[1])
    elif argv[3].startswith('page'):
        extract_site()

# todo: infinite loop
