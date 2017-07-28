#!/usr/bin/env python
from pymongo import MongoClient
import bson
import bson.json_util
import json
import sys

#get all frontpaged variants in mongodb, db CR, panelvcf
#include acmg score for the variants from nucvariant
#bifx@courtagen, jje, jw	11062015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''


host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
limit = 0
collection = 'panelvcf'
collection_nv = "nucvariants"
collection_rprtver = "report_versions"

#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]
m_collect_nv = m_db[collection_nv]
m_collect_rprtver = m_db[collection_rprtver]


filter = {'variantlist.frontpage':True}
#attrib = {'gpp':True, 'panel':True, 'panel_version':True, 'variantlist.driver':True, 'variantlist.variant_id':True}
attrib = None
desired = ['_id', 'gpp', 'panel', 'panel_version', 'pt_id']#and variantlist.driver, variantlist.variant_id

for record in m_collect.find(filter, attrib).limit(limit):
	#json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))
	#rec = bson.json_util.dumps(record)
	#if 'pt_id' in record and record['pt_id'] != 1039:
	#	continue
	rprt = record['_id']
	used = m_collect_rprtver.find_one({'_id': record['gpp'], 'use': record['_id']}, {'use':True})
	
	if used is not None and used['use'] is not None and 'variantlist' in record:
	
		for variant in record['variantlist']:
			if 'frontpage' in variant and variant['frontpage'] is True:
				info = list()
				
				for desire in desired:
					try:
						info.append(str(record[desire]))
					except:
						info.append(str(None))

				info.append(str(variant['variant_id']))
				
				acmg = m_collect_nv.find_one({'variant_id': str(variant['variant_id'])}, {'locked_down_variantscore': True})
				if acmg is not None and 'locked_down_variantscore' in acmg and acmg['locked_down_variantscore'] is not None:
					info.append(str(acmg['locked_down_variantscore']))
				else:
					info.append(str(None))
					
				print "\t".join(info)
exit()
