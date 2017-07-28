#!/usr/bin/env python
from pymongo import MongoClient
import re
import sys

#get variant science notes in mongodb, db CR, nucvariants
#bifx@courtagen, jje, jw	11062015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''


host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
limit = 0

try:#collection name required
	collection = sys.argv[1]
except:
	print "usage: cr_find_vsn.py collection\n  additional args: host(optional,"+",".join(host)+") port(optional,"+port+") db(optional,"+db+")"
	exit(1)
	
try:
	host = sys.argv[2]
except:
	host = host
try:
	port = sys.argv[3]
except:
	port = port
try:
	db = sys.argv[4]
except:
	db = db


#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]


#get records with locked_down_notes, parse out $$ contents
for mut in m_collect.find({'variant_science_notes':{'$exists':'true'}},{'variant_science_notes':'true'}).limit(limit):
	
	vsn = mut['variant_science_notes'].encode('utf8').decode("ascii","ignore").rstrip().replace('\n',' ')
	print mut['_id'] + '\t' + vsn

exit()
