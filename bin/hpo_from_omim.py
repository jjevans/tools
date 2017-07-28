#!/usr/bin/env python
import hpo_db
import sys

database = "hpo0"
username = "python"
hostname = "localhost"

#omimid = 614200
try:
	omimid = sys.argv[1]
except IOError as (errno,strerr):
	print "hpo_from_omim.py omim_phenotype_id"

hpo_obj = hpo_db.HPO(database,username,hostname)
answer = hpo_obj.pheno_by_omim(omimid)
hpo_obj.print_ans(answer)
