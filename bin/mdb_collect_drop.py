#!/usr/bin/env python
from pymongo import MongoClient
from pymongo.errors import WriteError
import re
import sys

do_drop = True

#mongodb drop existing collection to new collection
#bifx@courtagen, jje, jw	11122015
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
limit = 0

#collection name required
try:
	collection = sys.argv[1]
except:
	message = "usage: mdb_collect_drop.py collection\n  additional args: host(optional,"+",".join(host)+") port(optional,"+port+") db(optional,"+db+")\n"
	sys.stderr.write(message) 
	exit(1)

try:#optional
	host = sys.argv[2]
	port = sys.argv[3]
	db = sys.argv[4]
except:
	pass

#get source collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]

#check source collection
if not collection in m_db.collection_names():#collection doesn't exist
	message = 'ERROR: collection not in database: ' + collection + '\n'
	sys.stderr.write(message)
	exit(1)

m_collect = m_db[collection]

#confirm delete on user input (must be y or yes)
answer = raw_input('delete collection? ' + collection + '?  (y or yes) ')
if answer != 'y' and answer != 'yes':
	message = "ERROR: answer requires 'y' or 'yes. die.\n"
	sys.stderr.write(message)
	exit(1)

#drop collection
if do_drop:
	#try:
	m_collect.drop()
	#except:
	#	message = 'ERROR: could not drop collection: ' + collection + '\n'
	#	sys.stderr.write(message)
	#	exit(1)
else:
	message = 'collection not dropped. do_drop=' + str(do_drop) + '\n'
	sys.stderr.write(message)
	
exit()
