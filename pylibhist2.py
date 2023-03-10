
print("Done!")

# Refactored code:
from functools import reduce
import requests
from bs4 import BeautifulSoup


def get_module_names(url):
    rsp = requests.get(url, verify=True, allow_redirects=True)
    soup = BeautifulSoup(rsp.text, features="html.parser")

    modules = soup.find_all("code", attrs={"class":"module"})

    return [module.text for module in modules]


def write_modules(file, modules):
    for module in modules:
        file.write(f"\t{module}\n")


def main():
    urls = ["https://docs.python.org/release/1.4/lib/", 
            "https://docs.python.org/release/1.5/lib/", 
            "https://docs.python.org/release/1.5.1/lib/", 
            "https://docs.python.org/release/1.5.1p1/lib/", 
            "https://docs.python.org/release/1.5.2/lib/" , 
            "https://docs.python.org/release/1.5.2p1/lib/",
            "https://docs.python.org/release/1.5.2p2/lib/",
            "https://docs.python.org/release/1.6/lib/",
            "https://docs.python.org/release/2.0/lib/",
    ]
    modules = reduce(urls, (lambda back, url: back.add(*get_module_names(url))), set())
    with open("python library history2.txt", "w+") as codex:
        write_modules(codex, modules)

main()