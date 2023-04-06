import requests
from bs4 import BeautifulSoup
base_url = "https://docs.python.org/release/{ver}/lib/"
vers = ["1.4", "1.5", "1.5.1", "1.5.1p1", "1.5.2",
         "1.5.2p1", "1.5.2p2", "1.6", "2.0"]

codex_nom = "python library history.txt"
with open(codex_nom, "w+") as file:
    pass

seen_modules = set()

for ver in vers:
    with open(codex_nom, "a") as file:
        file.write(ver + ":\n")

    url = base_url.format(ver)
    rsp = requests.get(url, verify=True, allow_redirects=True)
    soup = BeautifulSoup(rsp.text, features="html.parser")
    body = soup.body
    moduli = body.find_all(["code", "tt"])
    with open(codex_nom, 'a') as file:
        for module in moduli:
            try:
                if module['class'][0] != "module":
                    continue
            except KeyError:
                pass
            module = module.text
            if module not in seen_modules:
                file.write(f"\t{module}\n")
                print(module)
                seen_modules.add(module)
        file.write("\n")
