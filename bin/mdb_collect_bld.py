#!/usr/bin/env python
from datetime import datetime, date, time
from pymongo import MongoClient
import re
import sys
#pull patient id, location from panelvcf and add to variant_queue collections
#bifx@courtagen, jje, jw	03222015
#import bson.json_util
#import json

'''from pymongo import MongoClient
import bson
import bson.json_util
import json
import os.path
import sys'''

#test if a gpp has a report in mongodb, db CR, panelvcf
#bifx@courtagen, jje, jw	01182015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
dbname = "CR"
collection0 = "variant_queue"
collection1 = "nucvariants"

def format_gpp(gpp):
	#leading GPP in panelvcf field gpp
	gpp = str(gpp)
	
	retstr = str()
	if not gpp.startswith('GPP'):
		retstr = 'GPP';
	retstr += gpp.rstrip()
	
	return retstr
def not_clia(loc):
	patterns = ['york', 'York', 'ny', 'NY']
	
	for pattern in patterns:
		if re.search(pattern, loc) is not None:
			return False
		
	return True

if __name__ == '__main__':
	
	#if sys.stdin.isatty() and len(sys.argv) == 1:#usage
	#	print "usage: cr_ptid_pvcf.py gpp/stdin list of gpps"
	#	exit(1)

	#get collection
	mongo = MongoClient(host,int(port))
	m_db = mongo[dbname]
	m_collect0 = m_db[collection0]
	m_collect1 = m_db[collection1]

lmt = 0

qry = dict()
qry["variant"] = None
#qry["failed"] = {"$not": {"$type": 10}} 
#qry["call"] = {"$not": {"$type": 10}} 


#{"gpp": 1, "gene": 1, "complete": 1, "failed": 1, "location": 1, "type": 1, "batch": 1, "call": 1, "ts": 1}
projection = dict()
#projection["_id"] = -1
#projection["gpp"] = 1
projection["genename"] = 1
#projection["complete"] = 1
#projection["failed"] = 1
#projection["location"] = 1
#projection["type"] = 1
#projection["batch"] = 1
#projection["call"] = 1
#projection["ts"] = 1


#for record in m_collect0.find(qry, projection).sort(srt).limit(lmt):
#for record in m_collect0.find(qry, projection).limit(lmt):
for record in m_collect0.find().limit(lmt):
	variant = record["variant"]
	chr, rest = variant.split("@")
	pos, ref, alt = rest.split("|")
	
	if "gene" in  record and record["gene"] is not None:
		#chr = record["chrom"]
		#pos = record["pos"]
		filts = {"chrom": chr, "pos": int(pos)}

		#nv_rec = m_collect1.find_one(filts)
		for nv_rec in m_collect1.find({"chrom":chr, "pos": int(pos)}):
	
			print str(chr) + "\t" + str(pos) + "\t" + nv_rec["genename"]
			newrec = dict(record)
		
			newrec.pop("_id")
			newrec["gene"] = nv_rec["genename"]
		
			try:
				m_collect0.save(newrec)
			except:
				print "ERROR SAVING RECORD: " + variant
			
	else:
		print "ERROR: variant " + variant + " has no gene in nucvariants"

exit()







				
	#newrec.pop("_id")
	#gpp =  unicode(newrec["gpp"])
#	variant = newrec["variant"]
	#nv_rec = m_collect1.find_one({'gpp': gpp})
#	nv_rec = m_collect1.find_one({'variant_id': variant})
	
#	if nv_rec is not None and 'variant_id' in nv_rec:
#		print str(nv_rec['variant_id']) + "\t" + str(nv_rec['genename'])
#	else:
#		print variant + "\t" + "none"

	#ts = record["ts"]
	#newrec.pop("ts")
	#newrec[unicode("created")] = ts
	#newrec[unicode("submitted")] = ts
#	m_collect1.save(newrec)
'''
	for record in m_collect0.find():
		gpp = format_gpp(record['gpp'])

		pvcf_rec = m_collect1.find_one({'gpp': unicode(gpp)})	
		if pvcf_rec is None:
			patient = 0 #carrier
		else:
			if 'pt_id' in pvcf_rec:
				patient = pvcf_rec['pt_id']
			else:
				sys.stderr.write(gpp +'\tNO_PT_ID\n')
				patient = -1

		record['patient'] = patient
		
		if 'pt_id' in record:
			del record['pt_id']
		#if pvcf_rec is None or not 'location' in pvcf_rec or pvcf_rec['location'] is None or ('location' in record and str(record['location']) != 'chug') or not_clia(str(pvcf_rec['location'])):
		#	loc = 'genewiz'
		#else:
		#	loc = 'chug'
		m_collect0.save(record)
'''
