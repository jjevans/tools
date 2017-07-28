#!/usr/bin/env python
from pymongo import MongoClient
import bson
from bson.codec_options import CodecOptions
import bson.json_util
import json
import sys


#run find query in mongodb, db CR, nucvariants
#bifx@courtagen, jje, jw	11062015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''


host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
limit = 0

try:#collection name required
	collection = sys.argv[1]
except:
	print "usage: cr_find.py collection\n\t(additional args key value by colon: _id=11259 key0=val0 key1=val1)"
	exit(1)

filter = dict()#criteria to find
attrib = dict()#keys to output
try:
	for arg in sys.argv[2:]:
		parts = arg.split('=')

		if len(parts) == 1:#if no arg put as output field
			attrib[parts[0]] = True
		else:
			
			if isinstance(parts[i], int):
				filter[parts[0]] = int(parts[1])
			else:
				filter[parts[0]] = parts[1]

except:
	pass
	
if not len(attrib):#print whole document
	attrib = None

#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]

m_opts = CodecOptions(unicode_decode_error_handler='ignore')#for bson decode

for record in m_collect.find(filter, attrib).limit(limit):

	try:
		try:
			print bson.dumps(record)
		except TypeError:#date parse prob
			print bson.BSON.decode(record, codec_options=m_opts)
		except:
			print bson.json_util.dumps(record)

	except:
		message = "bson parse failure: " + record['_id']
		raise Exception(message)
		
	
exit()
