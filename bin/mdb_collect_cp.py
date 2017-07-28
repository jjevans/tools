#!/usr/bin/env python
from pymongo import MongoClient, DESCENDING
from pymongo.errors import WriteError
import re
import sys

'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''

#mongodb copy existing collection to new collection
#bifx@courtagen, jje, jw	11062015
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
limit = 0

#if len(sys.argv) != 4:
usage = "usage: mdb_collect_cp.py source_collection target_collection\n  additional args: host(optional,"+",".join(host)+") port(optional,"+port+") db(optional,"+db+")"


#source and target collections
try:
	src = sys.argv[1]
	target = sys.argv[2]
except:
	print usage
	exit(1)

try:#optional
	host = sys.argv[3]
	port = sys.argv[4]
	db = sys.argv[5]
except:
	pass

#get source collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]

#check source collection
if not src in m_db.collection_names():#collection doesn't exist
	message = 'ERROR: source collection not in database: ' + collection + '\n'
	sys.stderr.write(message)
	exit(1)

elif src == target:#error if source and target collections same
	message = 'ERROR: source collection the same as target collection'
	sys.stderr.write(message)
	exit(1)

#error if target collection already exists
if target in m_db.collection_names():
	message = 'ERROR: target collection already exists: ' + target + '\n'
	sys.stderr.write(message)
	exit(1)

m_src = m_db[src]
m_target = m_db[target]

#get records with locked_down_notes, parse out $$ contents
#for record in m_src.find().sort([('seq_creation_ts', DESCENDING)]).limit(limit):
for record in m_src.find().limit(limit):
	
	try:
		pass
		m_target.update_one({'_id':record['_id']}, {'$set':record}, upsert=True)
	except WriteError:
		print 'ERROR (pymongo.errors.WriteError): ' + record['_id']

exit()
