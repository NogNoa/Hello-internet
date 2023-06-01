import os
from dataclasses import dataclass
from sys import argv

import requests

from TableRead import *
import bs4
import logging

root_scheme = "https://"
logging.basicConfig(filename="extract-site.log")


@dataclass
class Link:
    scheme: str  # terminating '://' is included
    domain: str
    path: str  # terminating '/' is guranteed on initialization
    base: str  # index.html is completed on read
    ext: str

    @staticmethod
    def from_string(link: str):
        link = link.partition("://")
        scheme, link = (link[0], link[2]) if link[2] else ("", link[0])
        link = link.partition("/")
        domain, link = (link[0], link[2]) if link[2] else ("", link[0])

    @property
    def url(self):
        return sum((self.scheme, self.domain, self.path, self.base, self.ext), "")

    @property
    def full_path(self):
        return self.domain + self.path

    @property
    def file_name(self):
        return self.base + self.ext or "index.html"

    @property
    def full_file_name(self):
        return sum((self.domain, self.path, self.file_name), "")


"""
types of links:
{scheme}://domain/path/base.ext
path/base.ext           === {local_path}/{<}
/path/base.ext          === {root_adress}{<}
{scheme}://domain/path/ === {<}index.html
{scheme}://domain/path  === {<}/index.html
path                    === {local_path}/{<}/index.html
path/                   === {local_path}/{<}index.html
/path                   === {root_adress}/{<}/index.html
/path/                  === {root_adress}/{<}index.html
"""


def path_build(codex_nom: str):
    folder_nom = ""
    for fldr in codex_nom.split("/")[:-1]:
        folder_nom += f"{fldr}/"
        print(f"folder: {folder_nom}")
        try:
            os.mkdir(folder_nom)
            print(folder_nom)
        except FileExistsError:
            pass


def save_as(name: str, inter: str = ''):
    if inter: inter = inter.rstrip("/") + "/"
    local_path = inter + name
    sleep(random.random() * 10)
    resp = requests.get(root_scheme + local_path)
    codex_nom = local_path
    if resp.text.lower().startswith(("<!doctype html>", "<html>")):
        if local_path == root_adress + "index.html":
            return
        extract_children(name, inter)
        if not name.endswith(".html"):
            codex_nom = local_path.rstrip("/") + "index.html"
    if os.path.exists(codex_nom) and os.path.getsize(codex_nom):
        print(codex_nom)
        return
    if name.split("/")[:-1]:
        path_build(local_path)
    with open(codex_nom, "wb+") as codex:
        codex.write(resp.content)
    print(codex_nom)


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
            if not isinstance(sub, bs4.NavigableString): extract_tag(sub, local_path)
        if tag.has_attr("href"):
            link = tag["href"]
        elif tag.has_attr("src"):
            link = tag["src"]
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
            path = "/".join(adrs[3:-1]) + "/"
            name = adrs[-1]
            save_as(path + name, domain)
        else:
            return
    elif link.startswith("/"):
        memory.add(root_adress + link)
        save_as(link)
    else:
        memory.add(local_path + link)
        save_as(link, local_path)


def extract_children(page: str, inter, wayback=False):
    soup: bs4.BeautifulSoup = soup_init(url=root_scheme + inter + page)
    if soup.html: soup = soup.html
    if wayback:
        soup = wayback_strip(soup)
    local_path = inter if page.endswith(".html") else inter.rstrip("/") + f"/{page}"
    for tag in soup:
        if not isinstance(tag, bs4.NavigableString): extract_tag(tag, local_path)


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
