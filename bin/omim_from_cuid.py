#!/usr/bin/env python
import umls_db
import sys

database = "umls"
username = "python"
hostname = "localhost"

try:
	cuid = sys.argv[1]
except IOError as (errno,strerr):
	print "omim_from_cuid.py umls_cuid"

umls_obj = umls_db.UMLS(database,username,hostname)
answer = umls_obj.omim_by_cuid(cuid)
umls_obj.print_ans(answer)
