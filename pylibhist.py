import requests
from bs4 import BeautifulSoup

urli = ["https://docs.python.org/release/1.4/lib/",
        "https://docs.python.org/release/1.5/lib/",
        "https://docs.python.org/release/1.5.1/lib/",
        "https://docs.python.org/release/1.5.1p1/lib/",
        "https://docs.python.org/release/1.5.2/lib/",
        "https://docs.python.org/release/1.5.2p1/lib/",
        "https://docs.python.org/release/1.5.2p2/lib/",
        "https://docs.python.org/release/1.6/lib/",
        "https://docs.python.org/release/2.0/lib/",
        ]

codex_nom = "python library history.txt"
with open(codex_nom, "w+") as file:
    pass

seen_modules = set()

for url in urli:
    version = url.split("/")[4]
    with open(codex_nom, "a") as file:
        file.write(version + ":\n")

    rsp = requests.get(url, verify=True, allow_redirects=True)
    soup = BeautifulSoup(rsp.text, features="html.parser")
    body = soup.body
    moduli = body.find_all(["code", "tt"])
    with open(codex_nom, 'a') as file:
        for module in moduli:
            try:
                cls = f" - {module['class'][0]}"
            except KeyError:
                cls = ''
            module = module.text
            if module not in seen_modules:
                file.write(f"\t{module}{cls}\n")
                print(module+cls)
                seen_modules.add(module)
        file.write("\n")
