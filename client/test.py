#!/usr/bin/env python3

import platform
import requests
import config
import psycopg2

from subprocess    import check_output
from cpe           import CPE
from pprint        import pprint
from pymongo       import MongoClient
from pkg_resources import parse_version

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

# TODO: remove test entry here
package_list.append({
  "name": "openssl",
  "version": "1.0.1b"
})

# set up DB connection
postgresConnection = psycopg2.connect(dbname=config.postgresql.dbname,
                                      user=config.postgresql.user,
                                      password=config.postgresql.password)
postgresCursor = postgresConnection.cursor()
#searchCveByProductQuery = "SELECT levenshtein(name,'{0}'), * FROM cve_per_product_version WHERE name ~ '{0}' AND levenshtein(name,'{0}') < 5"
searchCveByProductQuery = "SELECT * FROM cve_per_product_version WHERE name = '{0}'"

for pkg in package_list:
  installedVersion = parse_version(pkg["version"])
  postgresCursor.execute(searchCveByProductQuery.format(pkg["name"]))

  for resultrow in postgresCursor:
      rowVersion = parse_version(resultrow[2])
      badVersionInstalled = rowVersion == installedVersion

      if badVersionInstalled:
        print(pkg["name"], " v", pkg["version"], " could be affected by ",  resultrow[0])
