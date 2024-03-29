import os
import re
import time
from dataclasses import dataclass
from sys import argv

import requests

from TableRead import *
import bs4
import logging

root_scheme = "https://"
logging.basicConfig(filename="extract-site.log", level="debug")
req_time = time.time()
code_dir_pattern = r"([\"'])((code|js|img|css)/.*?)\\?\1"


@dataclass
class Link:
    scheme: str  # terminating '://' is included
    domain: str  # terminating '/' is guranteed on initialization if not empty
    local: str  # ""
    path: str  # ""
    base: str  # index.html is completed on read
    ext: str  # "" ext with the dot

    @staticmethod
    def from_string(link: str, local_path=""):
        # local path without the domain. terminated by "/" if not empty
        link = link.partition("://")
        if link[2]:
            scheme, link = link[0], link[2]
            scheme += "://"
            domain, _, link = link.partition("/")
            domain += "/"
        else:
            scheme = root_scheme
            domain = root_link.domain
            link = link[0]
            if link.startswith("/"):
                link = link.strip("/")
                local_path = ""
        if link.startswith(".."):
            if local_path:
                local_path = "/".join(f"{local_path}".split("/")[:-2]) + "/"
                link = link.strip("./")
            else:
                logging.error("".join((scheme, domain, local_path, link)))
        link = link.rsplit("/", 1)
        if len(link) == 2 and link[1]:
            path, file = link[0], link[1]
        else:
            path, file = ("", link[0]) if ("." in link[0]) else (link[0], "")
        if file == "..":
            path = "/".join(f"{path}".split("/")[:-2])
            file = ""
        base, _, ext = file.partition(".")
        if ext: ext = "." + ext
        if path: path = path.rstrip("/") + "/"
        return Link(scheme, domain, local_path, path, base, ext)

    @property
    def url(self):
        return self.scheme + self.full_file_name

    @property
    def inter(self):
        return self.local + self.path

    @property
    def full_path(self):
        return self.domain + self.inter

    @property
    def file_name(self):
        return self.base + self.ext

    @property
    def full_file_name(self):
        return self.full_path + self.file_name


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
base.ext                === {local_path}/{<}
/base.ext               === {root_adress}{<}
path/extentionless
"""


def path_build(path: str):
    try:
        os.makedirs(path)
        print(f"folder: {path}")
    except FileExistsError:
        pass


def save_as(page: Link, wayback: bool):
    global req_time
    if os.path.exists(page.full_file_name) and os.path.getsize(page.full_file_name):
        print(page.full_file_name)
        return
    sleep(random.random() + max((0, req_time + 4 - time.time())))
    resp = requests.get(page.url)
    if resp.status_code != 200 and page.local:
        page.local = ""
        sleep(random.random() + max((0, req_time + 4 - time.time())))
        resp = requests.get(page.url)
        if resp.status_code != 200:
            print(f"connection error: {page.url}")
            return
    req_time = time.time()
    if page.ext == ".html" or resp.text.lower().startswith(("<!doctype html>", "<html>")):
        if not page.ext:
            page.path = (page.path + page.base).rstrip("/") + "/"
            page.base, page.ext = "index", ".html"
        extract_children(page, wayback)
    elif page.ext == ".js":
        print(page.url)
        extract_js(resp.text, page.inter, wayback=wayback)
    if not page.base:
        page.path = page.path.split("/")
        page.base = page.path[-2]
        page.path = "/".join(page.path[:-2])
        if page.path: page.path += "/"
    if os.path.exists(page.full_file_name) and os.path.getsize(page.full_file_name):
        print(page.full_file_name)
        return
    path_build(page.full_path)
    with open(page.full_file_name, "wb+") as codex:
        codex.write(resp.content)
    print(page.full_file_name)


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


def extract_directory(local_path: str = "", wayback=False):
    soup = soup_init(url=local_path)
    try:
        os.mkdir(local_path)
    except FileExistsError:
        pass
    if wayback:
        soup = wayback_strip(soup)
    for img in soup.body.find_all("img"):
        link = img.next.next["href"]
        if not link:
            print(f'url="{local_path}", element="{img.next}"')
            continue
        file = Link.from_string(link, local_path)
        suffix = img["src"].split("/")[-1]
        if suffix in {"unknown.gif", "compressed.gif", "tar.gif"}:
            save_as(file, wayback)
        elif suffix == "folder.gif":
            extract_directory(local_path + link)
        elif suffix in {"blank.gif", "back.gif"}:
            pass
        else:
            print(suffix)


def extract_tag(tag: bs4.element, local_path='', wayback: bool = False):
    try:
        for sub in tag.children:
            if not isinstance(sub, bs4.NavigableString): extract_tag(sub, local_path)
        if tag.has_attr("href"):
            extract_link(tag["href"], local_path, wayback, )
        elif tag.has_attr("src"):
            extract_link(tag["src"], local_path, wayback, )
        elif tag.name == "script":
            extract_js(tag.text, local_path, wayback)
    except AttributeError:
        return


def extract_link(link: str, local_path: str = "", wayback: bool = False):
    link = link.partition("#")[0].partition("?")[0]
    if link:
        link = Link.from_string(link, local_path)
    else:
        return
    if link.domain != root_link.domain or link.full_file_name in memory:
        return
    memory.add(link.full_file_name)
    save_as(link, wayback)


def extract_js(script: str, local_path: str = "", wayback: bool = False):
    if fldri := re.findall(code_dir_pattern, script):
        for link in (fldr[1] for fldr in set(fldri)):
            extract_link(link, local_path, wayback)


def extract_children(page: Link, wayback=False):
    soup: bs4.BeautifulSoup = soup_init(url=page.url)
    if soup.html: soup = soup.html
    if wayback:
        soup = wayback_strip(soup)
    for tag in soup:
        if not isinstance(tag, bs4.NavigableString): extract_tag(tag, page.inter)


def extract_site(wayback=False):
    codex_nom = root_link.full_file_name
    path_build(root_link.full_path)
    soup: bs4.BeautifulSoup = soup_init(url=root_link.url)
    if soup.html: soup = soup.html
    if wayback:
        soup = wayback_strip(soup)
    for tag in soup:
        if not isinstance(tag, bs4.NavigableString): extract_tag(tag, root_link.path, wayback)
    with open(codex_nom, "w+", encoding="utf-8") as codex:
        codex.write(str(soup))
    print(codex_nom)


if __name__ == "__main__":
    root_link = Link.from_string(argv[1])
    root_link.scheme = root_link.scheme or root_scheme
    memory = {root_link.full_file_name, root_link.full_file_name + "index.html", "/"}
    os.chdir(argv[2])
    if argv[3].startswith('dir'):
        extract_directory(root_link.full_path)
    elif argv[3].startswith('page'):
        extract_site()

# todo: mailto:
