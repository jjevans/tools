#!/usr/bin/env python
from pymongo import MongoClient
import re
import sys


#pull out locked down notes in mongodb, db CR, nucvariants,
# parse out variant science notes from locked_down_notes which 
# are enclosed by double dollas ($$).  update record with field 
# variant_science_notes and variant_science_notes_history
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''
#get 'locked_down_notes' from nucvariant collection of mongo CR db
#bifx@courtagen, jje, jw	11062015


#print output and/or optionally make no modifications to collection for testing
do_print = False
do_upsert = True
do_summarize = True
limit = 0

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"


try:#collection name required
	collection = sys.argv[1]
except:
	print "usage: cr_vsn_from_ldn.py collection\n  additional args: host(optional,"+",".join(host)+") port(optional,"+port+") db(optional,"+db+")"
	exit(1)
	
try:
	host = sys.argv[2]
	port = sys.argv[3]
	db = sys.argv[4]
except:
	pass

#regex
regex = re.compile('\$\$.+?\$\$')

#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
m_collect = m_db[collection]

num_found = 0
num_done = 0

#get records with locked_down_notes, parse out $$ contents, make notes all one line
for mut in m_collect.find({'locked_down_notes':{'$exists':'true'}},{'locked_down_notes':'true'}).limit(limit):
	
	ldn = mut['locked_down_notes'].encode('utf8').decode("ascii","ignore").rstrip().replace('\r\n','\n').replace('\n',' ')

	#vsn_match = regex.search(ldn)
	vsn_match = regex.findall(ldn)
	
	#warn if multiple matches
	if len(vsn_match) > 1:
		message = 'Warning: multiple matches of $$ pairs: '  + mut['_id'] + '\n'
		sys.stderr.write(message)
	
	#use all cases of matches to 
	#retrieve variant science notes
	if len(vsn_match) > 0:

		#remove variant science notes from locked down notes
		#ldn = ldn.replace(vsn_match[0],'')
		
		#strip dolla signs
		vsn = vsn_match[0].strip('$')
		
  		upsert_this = {'locked_down_notes':ldn, 'variant_science_notes':vsn, 'variant_science_notes_history':[vsn]}

		if do_print:
			print mut['_id'] + '\t' + vsn + '\t' + ldn

		if do_upsert:#optional		
			m_collect.update_one({'_id':mut['_id']}, {'$set':upsert_this})

			num_done += 1

		num_found += 1
		
if do_summarize:#info
	if not do_upsert:
		sys.stderr.write('Info: no modifications made to mongo collection ' + collection + ', do_upsert=' + str(do_upsert) + ', Number found: ' + str(num_found) + '\n')
	else:
		sys.stderr.write('Info: number found: ' + str(num_found) + ', number of upserts made to collection ' + collection + ': ' + str(num_done) + '\n')
	
exit()
