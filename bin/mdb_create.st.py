#!/usr/bin/env python
from pymongo import MongoClient, DESCENDING
from pymongo.errors import WriteError
import random
import re
import sys

'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''

#mongodb copy existing collection to new collection
#bifx@courtagen, jje, jw	11062015
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
#limit = 1000
limit = 0

mongo = MongoClient(host,int(port))
m_db = mongo[db]

src = "sanger_tracking"

#check source collection
if not src in m_db.collection_names():#collection doesn't exist
	message = 'ERROR: source collection not in database: ' + collection + '\n'
	sys.stderr.write(message)
	exit(1)

m_src = m_db[src]

#get records with locked_down_notes, parse out $$ contents
for record in m_src.find({}).sort([("updated_at", DESCENDING)]).limit(limit):
	newrec = dict()
	newrec["gpp"] = str(record["_id"])
	try:
		newrec["reason"] = str(record["type"])
	except:
		next
	if "location" in record:
		newrec["location"] = str(record["location"])
	else:
		newrec["location"] = "unknown"

	if "variants_n_primers" in record:
		for mut in record["variants_n_primers"]:
			print newrec["gpp"]+'\t'+newrec['reason']+'\t'+str(mut)
			
	
'''	
	try:
		m_target.update_one({'_id':record['_id']}, {'$set':record}, upsert=True)
	except WriteError:
		print 'ERROR (pymongo.errors.WriteError): ' + record['_id']
'''
exit()
