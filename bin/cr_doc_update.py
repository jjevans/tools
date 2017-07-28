#!/usr/bin/env python
from datetime import datetime, date, time
from pymongo import MongoClient
import re
import sys
#change gpp id in collection panelvcf by prepending 'GPP' to 5-digit int id
#bifx@courtagen, jje, jw	04192016
'''from pymongo import MongoClient
import bson
import bson.json_util
import json
import os.path
import sys'''
do_save = True

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
dbname = "CR"
collection0 = "panelvcf"

def format_gpp(gpp):
	#leading GPP in panelvcf field gpp
	gpp = str(gpp)
	
	retstr = str()
	if not gpp.startswith('GPP'):
		retstr = 'GPP';
	retstr += gpp.rstrip()
	
	return retstr

if __name__ == '__main__':
	
	#if sys.stdin.isatty() and len(sys.argv) == 1:#usage
	#	print "usage: cr_ptid_pvcf.py gpp/stdin list of gpps"
	#	exit(1)

	#get collection
	mongo = MongoClient(host,int(port))
	m_db = mongo[dbname]
	m_collect0 = m_db[collection0]

	for record in m_collect0.find():
		try:
			gpp = format_gpp(record['gpp'])
			print "gpp before and after: " + record['gpp'] + "\t" + gpp
			
			if record['gpp'] != gpp and do_save:
				record['gpp'] = gpp
				info = m_collect0.save(record)
				print "gpp saved: " + gpp +  " " + str(info)
		except:
			sys.stderr.write("ERROR: couldn't update gpp for document: " + record['_id'] + "\n")
				
	exit()
	