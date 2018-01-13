#!/usr/bin/env python3

import platform
import requests
import config
import psycopg2
import sys

from cpe           import CPE
from pprint        import pprint
from pymongo       import MongoClient
from pkg_resources import parse_version

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
else:
  print("Unsupported distribution right here!", file=sys.stderr)
  exit(1)

# TODO: remove test entry here
package_list = [{
  "name": "openssl",
  "version": "1.0.1b"
}]

# set up DB connection
postgresConnection = psycopg2.connect(dbname=config.postgresql.dbname,
                                      user=config.postgresql.user,
                                      password=config.postgresql.password)
postgresCursor = postgresConnection.cursor()

affected_packages = []
searchCveByProductQuery = "SELECT cveid,name,version FROM cve_per_product_version WHERE name = '{0}'"
cveInformationQuery     = "SELECT id,cweid,summary,cvss,published FROM cve WHERE id = '{0}'"

bestReferenceQuery      = """
SELECT reference, refshare, nrefs, nrefstotal
FROM view_nist_reference_cwe_ranking nrcr
JOIN view_cvereference_extracted_domains crd ON crd.domain = nrcr.domain
WHERE nrcr.cweid = {0} AND crd.cveid = '{1}'
ORDER BY refshare DESC
LIMIT 1"""

bestUserQuery = "SELECT username, t_cwe_count / t_count::float AS rank, t_count FROM view_twitter_user_ranking WHERE cweid = {0} ORDER BY rank DESC LIMIT 1"

for pkg in package_list:
  print("...processing...", end="\r")

  installedVersion = parse_version(pkg["version"])
  postgresCursor.execute(searchCveByProductQuery.format(pkg["name"]))

  package_cves = []
  for resultrow in postgresCursor:
      rowVersion = parse_version(resultrow[2])
      badVersionInstalled = rowVersion == installedVersion

      if badVersionInstalled:
        package_cves.append(resultrow[0])

  if len(package_cves) > 0:
    affected_packages.append({
      "name": pkg["name"],
      "version": pkg["version"],
      "cves": package_cves
    })

    print(pkg["name"], "is affected by", len(package_cves), "known vulnerabilities")

print("DONE")
print()
print()

for affected in affected_packages:
  print(color.BOLD + affected["name"] + color.END)
  print("As of version" + affected["version"] + ", this package is affected by",
        len(affected["cves"]), "weaknesses. They are listed in detail below")

  for cve in affected["cves"]:
    postgresCursor.execute(cveInformationQuery.format(cve))
    info = postgresCursor.fetchone()
    
    print(color.RED + info[0] +  color.END, 'released on', info[4].strftime("%A %d. %B %Y"))
    print(info[2])
    print("Official NIST entry: https://nvd.nist.gov/vuln/detail/" + info[0])
   
    if info[1]: # some CVEs do not have an assigned CWE
      postgresCursor.execute(bestReferenceQuery.format(info[1], cve))
      bestReference = postgresCursor.fetchone()
    
      if bestReference:
        print("Recommended information source (" + str(round(bestReference[1],3)) + "% of total references for this CWE):", bestReference[0])

      postgresCursor.execute(bestUserQuery.format(info[1]))
      tweeter = postgresCursor.fetchone()

      if tweeter:
        print("A knowledgeable Twitter and Github user might be: https://github.com/" + tweeter[0], "-", str(round(tweeter[1],3)), "% of his posts are on this kind of CWE")
      
    print()
