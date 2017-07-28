#!/usr/bin/env python
from pymongo import MongoClient
import sys

#pull out gpp and primer used in sanger_submissions collection of mdb CR
#bifx@courtagen, jje, jw	08172016
'''$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")'''

host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"
collection_st = "sanger_tracking"
collection_ss = "sanger_submissions"
limit = 0

#get collection
mongo = MongoClient(host,int(port))
m_db = mongo[db]
st_collect = m_db[collection_st]
ss_collect = m_db[collection_ss]

#get records with locked_down_notes, parse out $$ contents
for proband in list(st_collect.find({'results':{'$exists':True}, 'type': {'$in': ['sanger confirmation', 'variant confirmation']}, 'carrier_relations':{'$exists':True}}).limit(limit)):

	if 'seqevents' in proband:
		for pb_seqevent in proband['seqevents']:
			if 'carrier_relations' in proband and len(list(ss_collect.find({'_id': pb_seqevent['seqid']}).limit(1))) > 0:
				for related in proband['carrier_relations']:
					relative = str(int(related))
					if int(related) != int(proband['_id']):

						cc_st = list(st_collect.find({'_id': str(relative)}).limit(1))

						if cc_st is not None and len(cc_st) > 0:

							cc_rec = dict(cc_st[0])

							if cc_rec is not None and 'seqevents' in cc_rec and len(cc_rec['seqevents']) > 0:

								for cc_seqevent in cc_rec[unicode('seqevents')]:
	 
									#was submitted and has variants in seqevent
									if 'variants_sequenced' in pb_seqevent and 'variants_sequenced' in cc_seqevent and len(list(ss_collect.find({'_id':cc_seqevent['seqid']}).limit(1))) > 0:

										for cc_variant in cc_seqevent['variants_sequenced']:

											if cc_variant in pb_seqevent['variants_sequenced']:

												cc_variant_rec = cc_seqevent['variants_sequenced'][cc_variant]
												if 'primers' in cc_variant_rec:
													cc_oligo = cc_variant_rec['primers'][0]

													if cc_variant in pb_seqevent['variants_sequenced'] and 'primers' in pb_seqevent['variants_sequenced'][cc_variant]:
														pb_oligo = pb_seqevent['variants_sequenced'][cc_variant]['primers'][0]

														if cc_oligo == pb_oligo:
															same_oligo = True
														else:
															same_oligo = False
															
														if 'results' in proband and cc_variant in proband['results'] and 'results' in cc_rec and cc_variant in cc_rec['results']:
															pb_call = proband['results'][cc_variant]
															cc_call = cc_rec['results'][cc_variant]
													
															if pb_call != cc_call:
																denovo = True
															else:
																denovo = False
														
															cc_res = cc_rec['results'][cc_variant]
															if cc_oligo in cc_res and 'failed' in cc_res[cc_oligo]:
																fail = cc_res[cc_oligo]['failed']#results back, rxn fail
															else:
																fail = False

															to_print = [proband['_id'], relative, cc_variant, str(denovo), pb_call, cc_call, str(same_oligo), str(pb_oligo), str(cc_oligo), str(fail), pb_seqevent['seqid'], cc_seqevent['seqid']]
												
															print '\t'.join(to_print)												

exit
