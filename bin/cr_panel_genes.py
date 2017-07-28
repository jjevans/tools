#!/usr/bin/env python
from pymongo import MongoClient
import bson
import bson.json_util
import json
import sys

#get all genes in each panel in mongodb, db CR, panels
#bifx@courtagen, jje, jw	11062015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''


host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
limit = 0
collection = 'panels'

#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]

for panel in m_collect.find().limit(limit):
	#json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))
	#rec = bson.json_util.dumps(record)
	#output = [panel['_id'], panel[]
	
	if 'genes' in panel:
		for gene in panel['genes']:

			print '\t'.join([str(gene['chr']), str(gene['start']), str(gene['end']), str(gene['hugoname']), str(panel['_id'])])

			#print panel['_id'] + '\t' +  '\t'.join(geneinfo)

#	else:
#		print panel['_id'] + '\tNone\tNone\tNone\tNone\tNone'	

exit()
