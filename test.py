#!/usr/bin/env python3

import platform
import requests
from subprocess import check_output

# check for linux distribution
distro = platform.linux_distribution()
package_list = []

# depending on distro load appropriate package for interfacing
# with package management mechanism
if distro[0] == "arch":
  import pacman
  package_list = [ {
    "id":p['id'],
    "name": p['id'],
    "version":p['version']
  } for p in pacman.get_installed() ]

elif distro[0] == 'debian':
  import apt
  cache = apt.Cache()

  for pkg in apt.Cache():
    if cache[pkg.name].is_installed:
      package_list.append({
        "name": pkg.name,
        "version": pkg.installed.version
      })

# do entity matching here

for pkg in package_list[0:50]:
  out = check_output(["/mnt/brick/home/fwolff/cve-search-master/bin/search_fulltext.py", "-q", pkg['name']]).splitlines()

  # acquire CVE information from database for every CVE
  cve_infos = []
  for cve in out:
    cveUrl = "http://127.0.0.1:5000/api/cve/{0}".format(cve)
    cveJson = requests.get(requestUrl).json()
    cve_infos.append(cveJson)

  # compare CVE critical version numbers with local version number

  print(pkg['name'], out)

