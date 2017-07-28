#!/usr/bin/env python
from pymongo import MongoClient
import sys

do_save = True

#change field  type in specified collection
#jje, jw	11122015
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"

#arg of -h, --help shows usage
#optional args of host ip(s), port, db (default CR)
if len(sys.argv) != 3:
	message = 'usage: cr_str_to_int.py collection field_to_change\n'
	sys.stderr.write(message)
	exit(1)

collection = sys.argv[1]
fld = sys.argv[2]

m_client = MongoClient(host,int(port))
m_db = m_client[db]
m_collect = m_db[collection]

for doc in m_collect.find({fld: {'$exists':True}}):
	val_str = doc[fld]
	
	try:
		val_int = int(val_str)
	except:
		message = "ERROR:  " + fld + " could not be coerced from string to integer."
		sys.write.stderr(message)
		continue
		
	doc[fld] = val_int
	if do_save:
		print str(doc['_id']) + "\t" + str(fld) + "\t" + str(val_str)
		m_collect.save(doc)
	else:
		print "INFO: '" + fld + "' option to save is value " + str(do_save) + " and is printed as a dry run.  field: " + fld
		
exit()
