#!/usr/bin/env python
from copy import deepcopy
from datetime import datetime, date, time
from pymongo import MongoClient

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
collection0 = "sanger_tracking"
collection1 = "variant_queue_0000"
collection2 = "variant_queue_1111"

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
	m_collect2 = m_db[collection2]
	
lmt = 0
srt = {"_id": -1}

#{ "failed": { $not: { $type: 10 } }, "call": { $not: { $type: 10 } } }
qry = dict()
#qry["failed"] = {"$not": {"$type": 10}} 
qry["gpp"] = None
qry["batch"] = None

#{"gpp": 1, "gene": 1, "complete": 1, "failed": 1, "location": 1, "type": 1, "batch": 1, "call": 1, "ts": 1}
'''projection = dict()
#projection["_id"] = -1
projection["gpp"] = 1
projection["gene"] = 1
projection["complete"] = 1
projection["failed"] = 1
projection["location"] = 1
projection["type"] = 1
projection["batch"] = 1
projection["call"] = 1
projection["ts"] = 1'''


#for record in m_collect0.find(qry, projection).sort(srt).limit(lmt):
for record in m_collect1.find().limit(lmt):
	#newrec = dict(record)
	#newrec.pop("_id")
#	st_rec = m_collect0.find_one({"seqevents.seqid": record["batch"], "_id": record["gpp"]})
	vq_rec = dict(record)
	print vq_rec["gpp"]


	record2 = m_collect0.find_one({"_id": str(vq_rec["gpp"])})
	st_rec = dict(record2)

	for se in st_rec["seqevents"]:
		#for i, vs in enumerate(se["variants_sequenced"]):
#		for i in xrange(se):
#			print str(i) + '\t' + se["variants_sequenced"]
		for variant in se["variants_sequenced"]:
		
			for primer in se["variants_sequenced"][variant]["primers"]:
				vq_rec[unicode("variant")] = variant
				vq_rec[unicode("primer")] = primer
				
				dc_rec = deepcopy(vq_rec)
				dc_rec.pop("_id")
				
				m_collect2.save(dc_rec)

#	print str(st_rec["_id"])
#	m_collect1.save()
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
exit()
	