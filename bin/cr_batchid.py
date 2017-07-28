#!/usr/bin/env python
from pymongo import MongoClient
import json
import sys

do_save = True

#get collections of mongo CR db
#jje, jw	11122015
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
collection = 'batchid_items'

usage = "usage: cr_batchid.py collection  mdb_key1  file1\n"
usage += "usage: cr_batchid.py collection  key1  file1 key2 file2\n"
usage += "\tnote: key2 and file2 optional\n"
usage += "\tfile format is one word per line with no spaces\n"
usage += "\tex:  word0,word1,word2\n"

try:
	collection = sys.argv[1]
	key0 = sys.argv[2]
	file0 = sys.argv[3]
	
	try:
		key1 = sys.argv[4]
		file1 = sys.argv[5]
	except:
		sys.stderr.write(usage + "\ncontinuing...") 
		
except:
	sys.stderr.write(usage)
	exit(1)
	
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]

with open(file0) as handle:
	itemstr0 = handle.read().rstrip()
	
items0 = itemstr0.split('\n')
doc = {key0: items0}

if key1 is not None:
	with open(file1) as handle:
		itemstr1 = handle.read().rstrip()
	items1 = itemstr1.split('\n')
	doc[key1] = items1

if do_save:
	m_collect.save(doc)
	sys.stderr.write('saving to collection...\n')
else:
	sys.stderr.write('no save to collection when var do_save = False\n')

sys.stderr.write('done.\n')

exit()
