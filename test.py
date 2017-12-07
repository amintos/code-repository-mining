#!/usr/bin/env python3

import platform
import requests

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
  requestUrl = "http://127.0.0.1:5000/api/cve/{0}".format(pkg['name'])
  cveJson = requests.get(requestUrl).json()
  print(pkg['name'], cveJson)

