#!/usr/bin/env python
from pymongo import MongoClient
import sys

#get collections of mongo CR db
#jje, jw	11122015
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"

#arg of -h, --help shows usage
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
	
mongo = MongoClient(host,int(port))
m_db = mongo[db]

print "\n".join(m_db.collection_names(include_system_collections=False))

exit()
