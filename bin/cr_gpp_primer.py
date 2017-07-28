#!/usr/bin/env python
from pymongo import MongoClient
import sys

#pull out gpp and primer used in sanger_submissions collection of mdb CR
#bifx@courtagen, jje, jw	08172016
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
collection = "sanger_submissions"
limit = 0

#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]

#get records with locked_down_notes, parse out $$ contents
for individual in m_collect.find({'GPPs':{'$exists':'true'}}).limit(limit):
	try:
		for rxn in individual['GPPs']:
			for gpp in rxn.keys():
				print str(gpp) + '\t' + str(rxn[gpp]['primer'])
	except:
		sys.stderr.write('ERROR: id ' + str(individual['_id']) + '\n')
		pass
exit()
