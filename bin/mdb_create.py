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
limit = 1000

mongo = MongoClient(host,int(port))
m_db = mongo[db]

src = "panelvcf"
target = "cube_b2"

#check source collection
if not src in m_db.collection_names():#collection doesn't exist
	message = 'ERROR: source collection not in database: ' + collection + '\n'
	sys.stderr.write(message)
	exit(1)

m_src = m_db[src]
m_target = m_db[target]

#get records with locked_down_notes, parse out $$ contents
for record in m_src.find({"success":True}).sort([("timestamp", DESCENDING)]).limit(limit):
	newrec = dict()
	newrec["gpp"] = record["gpp"]
	newrec["patient"] = record["pt_id"]
	newrec["variant"] = record["variantlist"]
	if "type" in record:
		newrec["reason"] = record["type"]
	else:
		newrec["reason"] = "unknown"
	if "location" in record:
		newrec["location"] = record["location"]
	else:
		newrec["location"] = "unknown"
	if "sangerconfirmsignoff" in record:
		newrec["complete"] = record["sangerconfirmsignoff"]
	else:
		newrec["complete"] = False

	num = random.randint(0,8)
	newrec["status"] = num

	#print "\t".join([str(newrec["gpp"]),str(newrec["patient"]), str(newrec["variant"]), str(newrec["reason"]), str(newrec["location"]), str(newrec["complete"]),str(newrec["status"])])
	print "\t".join([str(newrec["gpp"]),str(newrec["patient"]), str(newrec["reason"]), str(newrec["location"]), str(newrec["complete"]),str(newrec["status"])])
	#print newrec
'''	
	try:
		m_target.update_one({'_id':record['_id']}, {'$set':record}, upsert=True)
	except WriteError:
		print 'ERROR (pymongo.errors.WriteError): ' + record['_id']
'''
exit()
