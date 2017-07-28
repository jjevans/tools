#!/usr/bin/env python
from pymongo import MongoClient
import bson
import bson.json_util
import json
import sys

#get all genes for driver variants in mongodb, db CR, panelvcf
#include acmg score for the variants from nucvariant
#bifx@courtagen, jje, jw	11062015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''


host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
limit = 0
collection = 'panelvcf'
collection_nv = "nucvariants"

def form_variants(variantlist, m_collect_nv):#get ids and genenames of driver variants	
	drivers = list()
	
	for variant in variantlist:
		driver = [None, None, None]

		if 'driver' in variant and variant['driver'] is not None:

			if 'variant_id' in variant:
				driver[0] = str(variant['variant_id'])
				
				acmg = m_collect_nv.find_one({'variant_id': str(variant['variant_id'])}, {'locked_down_variantscore': True})
				if acmg is not None and 'locked_down_variantscore' in acmg and acmg['locked_down_variantscore'] is not None:
					driver[2] = str(acmg['locked_down_variantscore'])
				else:
					driver[2] = str(None)

			if 'genename' in variant:
				driver[1] = str(variant['genename'])
	
			drivers.append(driver)
			
	return drivers


#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]
m_collect_nv = m_db[collection_nv]

filter = None
#attrib = {'gpp':True, 'panel':True, 'panel_version':True, 'variantlist.driver':True, 'variantlist.variant_id':True}
attrib = None
desired = ['_id', 'gpp', 'panel', 'panel_version', 'pt_id']#and variantlist.driver, variantlist.variant_id

for record in m_collect.find(filter, attrib).limit(limit):
	#json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))
	#rec = bson.json_util.dumps(record)
	#if 'pt_id' in record and record['pt_id'] != 1039:
	#	continue
	
	if 'variantlist' in record:
		info = list()
	
		drivers = form_variants(record['variantlist'], m_collect_nv)
		
		if len(drivers) > 0:
			for desire in desired:
			
				if desire in record:
					info.append(str(record[desire]))
				else:
					info.append(str(None))

			for driver in drivers:
				print '\t'.join(info) + '\t' + '\t'.join(driver)

exit()
