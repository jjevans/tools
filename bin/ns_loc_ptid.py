#!/usr/bin/env python
from datetime import datetime, date, time
from pymongo import MongoClient
import re
import sys
#pull patient id, location from panelvcf and add to variant_queue collections
#bifx@courtagen, jje, jw	03222015

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
dbname = "CR"
collection0 = "variant_queue_1111"
#collection1 = "panelvcf"

rectype = "customrecord_gen_gpr"
ids = list()
fields = ["custrecord_gpp_patient_id"]

def format_gpp(gpp):
	#leading GPP in panelvcf field gpp
	gpp = str(gpp)
	
	retstr = str()
	if not gpp.startswith('GPP'):
		retstr = 'GPP';
	retstr += gpp.rstrip()
	
	return retstr

def not_ny(loc):
	patterns = ['york', 'York', 'ny', 'NY']
	
	for pattern in patterns:
		if re.search(pattern, loc) is not None:
			return True
		
	return False

if __name__ == '__main__':
	
	#if sys.stdin.isatty() and len(sys.argv) == 1:#usage
	#	print "usage: cr_ptid_pvcf.py gpp/stdin list of gpps"
	#	exit(1)

	#get collection
	mongo = MongoClient(host,int(port))
	m_db = mongo[dbname]
	m_collect0 = m_db[collection0]

	for record in m_collect0.find():
		gpp = format_gpp(record['gpp'])

		ns_args = args = {"rt".to_sym=>rectype, "id".to_sym=>gpp, "flds".to_sym=>fields}
		response = NS_get_fields_multi(args)
		print gpp + "\t" + str(response["custrecord_gpp_patient_id"])
#		m_collect0.save(record)

	exit()
	