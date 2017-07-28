#!/usr/bin/env python
import umls_db
import sys

database = "umls"
username = "python"
hostname = "localhost"

#omimid = 614200
try:
	omimid = sys.argv[1]
except IOError as (errno,strerr):
	print "cuid_from_omim.py omim_id"

umls_obj = umls_db.UMLS(database,username,hostname)
answer = umls_obj.cuid_by_omim(omimid)
umls_obj.print_ans(answer)
