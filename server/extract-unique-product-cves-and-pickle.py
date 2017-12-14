#!/usr/bin/env python3

import pickle
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client['cvedb']
collection = db['cve-search']


