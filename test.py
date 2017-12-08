#!/usr/bin/env python3

import platform
import requests
from subprocess import check_output
from cpe import CPE
from pprint import pprint

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

package_list = [{
    "name": "gcc",
    "version": "7.2.0-3"
}]
pkg_cves = dict()

for pkg in package_list:
    #out = check_output(["/mnt/brick/home/fwolff/cve-search-master/bin/search_fulltext.py", "-q", pkg['name']]).splitlines()
    out = check_output(["/home/felix/cve-search/bin/search_fulltext.py", "-q", pkg['name']]).splitlines()
    out = [ o.decode("utf-8") for o in out ]

  # acquire CVE information from cve-search API for every CVE
  cve_infos = []
  for cve in out:
      cveUrl = "http://127.0.0.1:5000/api/cve/{0}".format(cve)
      cveJson = requests.get(cveUrl).json()

    if cveJson != None:
        cve_infos.append(dict(cveJson))

  if len(cve_infos) > 0:
      print(pkg['name'], "matches these CPEs:")

  # compare CVE critical version numbers with local version number
  for cve in cve_infos:
      try:
          cpe_str = cve["vulnerable_configuration_cpe_2_2"][0]
          cve_cpe = CPE(cpe_str)
          print("\t",cve_cpe)
      except:
          print("bad cve_cpe")
          # it can happen that the vulnerable configuration array is empty!
