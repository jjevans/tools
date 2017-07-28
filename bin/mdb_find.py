#!/usr/bin/env python
from pymongo import MongoClient
import re
import sys

#pull out locked down notes in mongodb, db CR, nucvariants
#bifx@courtagen, jje, jw	11062015
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
criteria = dict()
limit = 0

try:#collection name required
	collection = sys.argv[1]
except:
	print 'usage: mdb_find.py collection\tquery_criteria(optional,ex. "_id:{\$exists:true}") host(optional,'+','.join(host)+') port(optional,'+port+') db(optional,'+db+')'
	exit(1)
	
try:
	criteria = {sys.argv[2]:{'$exists':True}}
	host = sys.argv[3]
	port = sys.argv[4]
	db = sys.argv[5]
except:
	pass

#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]

#get records with locked_down_notes, parse out $$ contents
for entry in m_collect.find(criteria):
	id = entry['_id'].decode('ascii','ignore')
	del entry['_id']
	
	line = str()
	for item in entry:#find type for each value

		if isinstance(item,list):
			type = 'Array'
		elif isinstance(item, dict):
			type = 'Subdocument (hash)'
		else:
			type = 'String'

		line += item.decode('ascii','ignore')  + ':' + type + ', '
		
	print id + '\t' + line.rstrip()

exit()
