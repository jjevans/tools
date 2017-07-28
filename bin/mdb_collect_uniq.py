#!/usr/bin/env python
from copy import deepcopy
from datetime import datetime, date, time
from pymongo import MongoClient
import re
import sys
#uniquify records (de-duplicates) in a collection
#bifx@courtagen, jje, jw	01182015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
dbname = "CR"

do_delete = True
lmt = 0
delim = ":::"

try:
	collection = sys.argv[1]
	tmp_collection = collection + '_tmp'
except:
	message = "mdb_collect_uniq.py collection_name_to_uniquify_documents\n"
	sys.stderr.write(message)
	exit(1)

mongo = MongoClient(host, int(port))
m_db = mongo[dbname]
m_collect = m_db[collection]

#flds = ["gpp", "patient", "variant", "gene", "type", "batch", "primer", "call", "created", "failed", "location", "submitted", "complete"]

uniqs = dict()
#ordered = list()
for record in m_collect.find().limit(lmt):
	doc = deepcopy(record)

	info = list()
	for fld in record.keys():
		if fld != '_id' and fld != 'created' and fld != 'submitted':
			info.append(str(record[fld]))
		
	doc_str = '""' + delim.join(info) + '""'
		
	if doc_str in uniqs:
		
		if do_delete:
			print "DELETE: " + str(record['_id']) + " remove duplicate document from collection."
			m_collect.delete_one({'_id': record['_id']})
		else:
			print "INFO: " + str(record['_id']) + " to be deleted except option do_delete is " + str(do_delete)
	else:
		print "INFO: " + str(record['_id']) + " is a unique entry and will be kept"
		uniqs[doc_str] = doc
#		ordered.append(doc_str)
		
'''
for order in ordered:
	print uniqs[order]
	
	if do_save:
		m_collect.save(uniqs[order])
'''

exit()
	