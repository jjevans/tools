#!/usr/bin/env python
import hpo_db
import sys

database = "hpo0"
username = "python"
hostname = "localhost"

try:
	cuid = sys.argv[1]
except IOError as (errno,strerr):
	print "hpo_from_omim.py umls_cuid"

hpo_obj = hpo_db.HPO(database,username,hostname)
answer = hpo_obj.pheno_by_umls(cuid)
hpo_obj.print_ans(answer)
