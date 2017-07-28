#!/usr/bin/env python
import copy
from pymongo import MongoClient
import sys

limit = 0

#in the case where the affected gpps do not exist in collection 
# variant_score_audit, get all gpps associated to a variant(s) in mongodb,
# db CR, panelvcf and backfill the audit trail in variant_score_audit
#bifx@courtagen, jje, jw	11062015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''


host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
collect_gpp = 'panelvcf'
#collect_audit = 'variant_score_audit_1'

try:
	collect_audit = sys.argv[1]
except:
	print 'usage: cr_assoc_gpp.py "variant_score_audit"_collection_to_mod'
	exit(1)

#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect_gpp = m_db[collect_gpp]
m_collect_audit =m_db[collect_audit]



#get all variants that have existing audit trail
#audit = list(m_collect_audit.find({'audits.gpps':{'$eq':None}},{'audits.gpps':True}).limit(limit))
need_gpps = m_collect_audit.find({'audits.gpps':{'$eq':None}},{'_id':True}).limit(limit)

combo = dict()
for needy in need_gpps:#all variants with audit of gpps is null
	id = str(needy['_id']) #variant id

	#get all associated gpps
	samples = m_collect_gpp.find({'variantlist.variant_id':id},{'gpp':True}).limit(limit)

	for sample in samples:
		gpp = str(sample['gpp'])

		if not id in combo:#init variant
			combo[id] = list()
		
		if gpp not in combo[id]:#only unique gpps
			combo[id].append(gpp)

	
for id in combo:
	gpps = ','.join(combo[id])

	variant = m_collect_audit.find_one({'_id':id},{'audits':True})
	audits = variant['audits']

	for i in range(0, len(audits)):#each audit

		try:
			if audits[i] is not None and audits[i]['gpps'] is None:
				fld_nm = 'audits.' + str(i) + '.gpps'
				m_collect_audit.update_one({'_id':id}, {'$set':{fld_nm: gpps}})
				print 'updated: ' + id + '\t' + str(i)
		except:
			sys.stderr.write('error: '+id+'\t'+str(i)+'\t'+str(audits[i])+'\n')

exit()
