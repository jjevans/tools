#!/usr/bin/env python
from pymongo import MongoClient
import sys

#cp a fields from one mongodb collection to another based on common _id
#jje, jw	04182016
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"

mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect0 = m_db['variant_queue_0002']
m_collect1 = m_db['variant_queue_0001']


exit()
