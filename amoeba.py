import os

import requests

from TableRead import *

root_adress = "https://web.archive.org/web/20060106073452/http://www.cs.vu.nl/pub/amoeba/"


def save_as(local_path):
    if os.path.exists(local_path) and os.path.getsize(local_path):
        return
    sleep(random.random()*10)
    resp = requests.get(root_adress + local_path)
    with open(local_path, "wb+") as codex:
        codex.write(resp.content)


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
        if suffix in {"unknown.gif", "compressed.gif", "tar.gif"}:
            save_as(local_path + link)
        elif suffix == "folder.gif":
            extract_directory(local_path + link)
        else:
            print(suffix)


if __name__ == "__main__":
    os.chdir(r"G:\Source\sites\Amoeba")
    extract_directory("amoeba5.3/")
