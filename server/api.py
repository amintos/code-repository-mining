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

import hug

postgresConnection = psycopg2.connect(dbname=config.postgresql.dbname,
                                      user=config.postgresql.user,
                                      password=config.postgresql.password)
postgresCursor = postgresConnection.cursor()

searchCveByProductQuery = "SELECT cveid,name,version FROM cve_per_product_version WHERE name = '{0}'"
cveInformationQuery     = "SELECT id,cweid,summary,cvss,published FROM cve WHERE id = '{0}'"

bestReferenceQuery      = """
SELECT reference, refshare, nrefs, nrefstotal
FROM view_nist_reference_cwe_ranking nrcr
JOIN view_cvereference_extracted_domains crd ON crd.domain = nrcr.domain
WHERE nrcr.cweid = {0} AND crd.cveid = '{1}'
ORDER BY refshare DESC
LIMIT 1"""

bestUserQuery = """
SELECT username, t_cwe_count / t_count::float AS rank, t_count
FROM view_twitter_user_ranking
WHERE cweid = {0}
ORDER BY rank DESC
LIMIT 1"""

@hug.get('/product-weaknesses')
def product_weaknesses(name, version):
  # determine all CVEs that this product is affected by
  installedVersion = parse_version(version)
  postgresCursor.execute(searchCveByProductQuery.format(name))

  package_cves = []
  for resultrow in postgresCursor:
      rowVersion = parse_version(resultrow[2])
      badVersionInstalled = rowVersion == installedVersion

      if badVersionInstalled:
        package_cves.append(resultrow[0])

  return_info = {
    "name": name,
    "version": version,
    "vulnerabilities": []
  }
  
  # no need to do anything when we have a good package
  if len(package_cves) == 0:
    return return_info

  for cve in package_cves:
    postgresCursor.execute(cveInformationQuery.format(cve))
    info = postgresCursor.fetchone()
    
    vulnerability = {
      "cveid": info[0],
      "released": info[4],
      "cweid": info[1],
      "description": info[2]
    }
   
    if info[1]: # some CVEs do not have an assigned CWE
      postgresCursor.execute(bestReferenceQuery.format(info[1], cve))
      bestReference = postgresCursor.fetchone()
      postgresCursor.execute(bestUserQuery.format(info[1]))
      tweeter = postgresCursor.fetchone()
    
      if bestReference:
        vulnerability["source_recommendation"] = bestReference[0]
        vulnerability["source_cwe_share"]      = round(bestReference[1],3)

      if tweeter:
        vulnerability["expert_recommendation"] = tweeter[0]
        vulnerability["expert_cwe_share"]     = round(tweeter[1],3)
    
    return_info["vulnerabilities"].append(vulnerability)

  return return_info
