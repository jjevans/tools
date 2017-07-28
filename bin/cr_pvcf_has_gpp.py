#!/usr/bin/env python
from pymongo import MongoClient
import bson
import bson.json_util
import json
import os.path
import sys

#test if a gpp has a report in mongodb, db CR, panelvcf
#bifx@courtagen, jje, jw	01182015
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
dbname = "CR"
collection = "panelvcf"

def format_gpp(gpp):
	#leading GPP in panelvcf field gpp
	retstr = str()
	if not gpp.startswith('GPP'):
		retstr = 'GPP';
	retstr += gpp.rstrip()
	
	return retstr

def gpp_list_exist(handle, db):
	#file handle to iterate over list of gpps
	#return list of two-tuple (gpp, True)
	output = list()
	for id in handle.readlines():
		gpp = format_gpp(id)
		found = gpp, gpp_exist(gpp, db)
		
		output.append(found)
		
	return output

def gpp_exist(gpp, db):
	#boolean if gpp exists in panelvcf collection db
	#gpp must start with GPP
	gpp = format_gpp(gpp)

	record = m_collect.find_one({'gpp':gpp})
	
	if record is None:#gpp not found
		return False
		
	return True
	
if __name__ == '__main__':
	
	if sys.stdin.isatty() and len(sys.argv) == 1:#usage
		print "usage: cr_pvcf_has_gpp.py gpp/stdin list of gpps"
		exit(1)

	#get collection
	mongo = MongoClient(host,int(port))
	m_db = mongo[dbname]
	m_collect = m_db[collection]
	
	try:#gpp as argument
		id = sys.argv[1]
		found = [(id, gpp_exist(id, m_collect))]

	except:#list of gpps on stdin
		found = gpp_list_exist(sys.stdin, m_collect)
		
	for gpp, in_pvcf in found:
		print gpp + '\t' + str(in_pvcf)
		
	exit()
	