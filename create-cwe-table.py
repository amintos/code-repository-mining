#!/usr/bin/env python3

import psycopg2
import config
import time
import re

from pymongo import MongoClient
from cpe     import CPE

createTableStatement ="""
CREATE TABLE cwe (
  cweid      INTEGER,
  name       VARCHAR(1024),
  status     VARCHAR(1024),
 weaknessabs VARCHAR(1024),
 description VARCHAR(16384),
 PRIMARY KEY (cweid)
);
"""
insertStatement = "INSERT INTO cwe VALUES(%s,%s,%s,%s,%s);"
dropTableStatement   = "DROP TABLE IF EXISTS cwe;"

postgresConnection = psycopg2.connect(dbname=config.postgresql.dbname,
                                      user=config.postgresql.user,
                                      password=config.postgresql.password)
postgresCursor = postgresConnection.cursor()

postgresCursor.execute(dropTableStatement)
postgresCursor.execute(createTableStatement)
postgresConnection.commit()

# set up MongoDB connection
mongoclient = MongoClient(config.mongodb.host, config.mongodb.port)
mongoCwes   = mongoclient['cvedb']['cwe']

# extract relevant data from every cve in the mongodb
# and write it into the newly created postgres table
cwecount = 0
for cwe in mongoCwes.find():
  row = (
      int(cwe["id"]),
      cwe["name"],
      cwe["status"],
      cwe["weaknessabs"],
      cwe["description_summary"]
    )

  cwecount += 1

  try:
    postgresCursor.execute(insertStatement, row)
  except:
    print(row)
    postgresConnection.commit()
    time.sleep(0.2)
    postgresCursor.execute(insertStatement, row)

print("Inserted ", cwecount, " CWEs")

postgresConnection.commit()
postgresCursor.close()
postgresConnection.close()
