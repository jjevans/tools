#!/usr/bin/env python
from pymongo import MongoClient
import sys

#sandbox to f' around with for mongo CR db
#jje, jw	04122016
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
collection = "variant_queue"

'''#arg of -h, --help shows usage
#optional args of host ip(s), port, db (default CR)
if len(sys.argv) > 1:
	
	if sys.argv[1] == '-h' or sys.argv[1] == '--help':
		message = 'usage: cr_collections.py\n  arg of -h, --help shows usage.\n  additional args: host(optional,[' + ','.join(host) + ']) port('+port+') db('+db+')\n'
		sys.stderr.write(message)
		exit(1)
	
	try:
		host = sys.argv[1]
		port = sys.argv[2]
		db = sys.argv[3]
	except:
		pass
'''
	
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]

for doc in m_collect.find({'notes':{'$exists':True}}, {'notes':True, 'notes_audit':True}):
	if 'notes_audit' in doc:
		for audit in doc['notes_audit']:
			print str(audit['user']) + '\t' + str(audit['ts']) + '\t\"' + str(audit['notes']) + '\"'
exit()
