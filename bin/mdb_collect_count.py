#!/usr/bin/env python
from pymongo import MongoClient
import re
import sys

'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''

#mongodb count records in collection given input query "{}"
#bifx@courtagen, jje, jw	11122015
criteria = dict()	
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"


#source and target collections
try:
	collection = sys.argv[1]
except:
	print "usage: mdb_collect_count.py collection\tfield(optional, exists)\n  additional args: host(optional,"+",".join(host)+") port(optional,"+port+") db(optional,"+db+")"
	exit(1)
	
try:
	criteria[sys.argv[2]] = {'$exists':True}
	host = sys.argv[3]
	port = sys.argv[4]
	db = sys.argv[5]
except:
	pass


#get source collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]

#error if collection doesn't exist
if not collection in m_db.collection_names():
	message = 'ERROR: collection not in database: ' + collection + '\n'
	sys.stderr.write(message)
	exit(1)

m_collect = m_db[collection]

#count records from collection
result = m_collect.find(criteria).count()
print str(result)
	
exit()
