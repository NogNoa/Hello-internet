import os
from sys import argv

import requests

from TableRead import *
import bs4

root_scheme = "https://"


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
                return


def save_as(name: str, inter: str = '', scheme: str = root_scheme):
    local_path = inter + name
    win_path = local_path.replace("?", "_")
    if os.path.exists(win_path) and os.path.getsize(win_path):
        print(local_path)
        return
    # if domain != scheme:
    #     try:
    #         os.makedirs(inter, )
    #     except FileExistsError:
    #         pass
    if name.split("/")[:-1]:
        path_build(local_path)
    sleep(random.random() * 10)
    resp = requests.get(scheme + local_path)
    with open(win_path, "wb+") as codex:
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
    if link in memory:
        return
    else:
        memory.add(link)
    if link.startswith("http"):
        adrs = link.split("/")
        scheme = "/".join(adrs[:2]) + "/"
        domain = (adrs[2]) + "/"
        path = "/".join(adrs[3:-1]) + "/"
        name = adrs[-1]
        if domain == root_adress:
            ext_func(name, domain+path, scheme=scheme)
        elif domain in root_adress:
            return
        else:
            save_as(name, domain+path, scheme)
    elif link.startswith("#"):
        return
    elif link.startswith("/"):
        ext_func(link)
    else:
        ext_func(link, local_path)


def extract_page(page: str, inter: str = '', wayback=False, **kwargs):
    inter = inter.rstrip('/') + '/'
    local_path = inter + page
    codex_nom = local_path.rstrip(".html") + ".html"
    if page.split("/"):
        path_build(local_path)
    soup: bs4.BeautifulSoup = soup_init(url=root_scheme + local_path)
    if soup.html: soup = soup.html
    if wayback:
        soup = wayback_strip(soup)
    for tag in soup:
        extract_tag(tag, local_path)
    with open(codex_nom, "w+", encoding="utf-8") as codex:
        codex.write(soup.text)
    print(local_path)


def extract_site(wayback=False, **kwargs):
    codex_nom = root_adress.rstrip("/") + "/index.html"
    path_build(codex_nom)
    soup: bs4.BeautifulSoup = soup_init(url=root_scheme + root_adress)
    if soup.html: soup = soup.html
    if wayback:
        soup = wayback_strip(soup)
    for tag in soup:
        extract_tag(tag, root_adress)
    with open(codex_nom, "w+", encoding="utf-8") as codex:
        codex.write(soup.text)
    print(codex_nom)


if __name__ == "__main__":
    root_adress = argv[1]
    root_scheme, _, root_adress = root_adress.partition("://")
    if root_adress:
        root_scheme += "://"
    else:
        root_adress = root_scheme
        root_scheme = "http://"
    memory = {root_adress, "/"}
    os.chdir(argv[2])
    if argv[3].startswith('dir'):
        extract_directory(argv[1])
    elif argv[3].startswith('page'):
        extract_page(argv[1])

# todo: infinite loop
