import requests
from bs4 import BeautifulSoup

url = "https://docs.python.org/release/1.4/lib/"

version = url.split("/")[4]
codex_nom = "python library history.txt"

with open(codex_nom, "a+") as file:
	file.write(version+":\n")

rsp = requests.get(url, verify=True, allow_redirects=True)
soup = BeautifulSoup(rsp.text, features="html.parser")
body = soup.body
moduli = body.find_all("code")
with open(codex_nom, "a+") as file:
	for module in moduli:
		file.write(f"\t{module.text}\n")
		print(module.text)
	file.write(2*"\n")