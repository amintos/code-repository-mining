#!/usr/bin/env python3

import platform
import requests
import sys
import dateutil.parser as timestamp_parser
from tqdm import tqdm

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def get_and_parse_json(pkg):
  api_url = "http://172.16.64.132:8000/product-weaknesses"
  r = requests.get(api_url, pkg)
  return r.json()

# check for linux distribution
distro = platform.linux_distribution()
package_list = []

# TODO depending on distro load appropriate package for interfacing
# with package management mechanism
if distro[0] == "arch":
  import pacman
  package_list = [ {
    "name":   p['id'],
    "version":p['version']
  } for p in pacman.get_installed() ]

elif distro[0] == 'debian':
  import apt
  cache = apt.Cache()

  for pkg in apt.Cache():
    if cache[pkg.name].is_installed:
      package_list.append({
        "name":    pkg.name,
        "version": pkg.installed.version
      })
else:
  print("Unsupported distribution right here!", file=sys.stderr)
  exit(1)

# TODO: remove test entry here
package_list = [
{
  "name": "openssl",
  "version": "1.0.1b"
},
{
  "name": "mac_os_x",
  "version": "10.9"
}]

print("We are analyzing", len(package_list), "packages on your system. This will take some time!", file=sys.stderr)

json_responses = []
pbar = tqdm(package_list, unit="package")
for pkg in pbar:
  pbar.set_description("Processing package {0} {1}".format(pkg["name"], pkg["version"]))
  pkg_info = get_and_parse_json(pkg)

  if len(pkg_info["vulnerabilities"]) > 0:
    json_responses.append(pkg_info)
pbar.close()

print("We scanned", len(package_list), "packages for vulnerabilities registered in the NIST database")
print("Of those packages", len(json_responses), "were affected by known vulnerabilities:")
for r in json_responses: print(r["name"])
print("---------------------------------------------------------------------------------------------")

for r in json_responses:
  print("Package", color.BOLD + r["name"] + color.END)
  print("As of your version", r["version"] + ", this package is affected by",
      len(r["vulnerabilities"]), "known weaknesses. They are listed in detail below:")
  print()

  for v in r["vulnerabilities"]:
    print(color.RED + v["cveid"] +  color.END, 'released on', timestamp_parser.parse(v["released"]).strftime("%A %d. %B %Y"))
    print(v["description"])
    print("Official NIST entry: https://nvd.nist.gov/vuln/detail/" + v["cveid"])

    if "source_recommendation" in v:
      print("Recommended information source (" + str(v["source_cwe_share"]) + "% of total references for this CWE):", v["source_recommendation"])

    if "expert_recommendation" in v:
      print("A knowledgeable Twitter and Github user might be: https://github.com/" + v["expert_recommendation"],
            "- as", str(v["expert_cwe_share"]) + "% of his posts are on this kind of CWE")

    print()

  print()
  print()
