#!/usr/bin/env python
from datetime import datetime, date, time
from pymongo import MongoClient
import re
import sys
#pull patient id, location from panelvcf and add to variant_queue collections
#bifx@courtagen, jje, jw	03222015

#do_save = True
do_save = False
limit = 0

'''from pymongo import MongoClient
import bson
import bson.json_util
import json
import os.path
import sys'''

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
dbname = "CR"
collection0 = "variant_queue"
collection1 = "panelvcf"

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
	if len(sys.argv) > 1:
		gpp_input = str(sys.argv[1])
	else:
		sys.stderr.write("INFO: doing all gpps in vq collect.\nNOTE: usage: gpp_ptid_pvcf.py gpp\n")
		gpp_input = None

	#get collection
	mongo = MongoClient(host,int(port))
	m_db = mongo[dbname]
	m_collect0 = m_db[collection0]
	m_collect1 = m_db[collection1]
	
	criteria = dict()
	if gpp_input is not None:
		criteria['gpp'] = int(gpp_input)

	for record in m_collect0.find(criteria).limit(limit):
		gpp = str(record['gpp'])
		pvcf_rec = m_collect1.find_one({'gpp': gpp})

		if pvcf_rec is None:#try with leadding GPP
			gpp = format_gpp(gpp)
			pvcf_rec = m_collect1.find_one({'gpp': gpp})
			pass

		if pvcf_rec is None:#none found
			sys.stderr.write('gpp record not in panelvcf: '+ str(gpp) + '\n')
			continue
    
		patient = pvcf_rec['pt_id']
		if patient is not None:
			print 'found: ' + str(gpp) + "\t" + str(patient)

			record['patient'] = int(patient)

			if do_save:
				m_collect0.save(record)
		else:
			sys.stderr.write('patient for gpp: ' + str(gpp) + ' not found\n')

	exit()
	
