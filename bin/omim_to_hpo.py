#!/usr/bin/env python
import hpo
import omim_api
import sys

# query omim for a term, take results and query omim for all genes for the 
# reported phenotypes and find the hpo phenotypes that match

# to reference hpo, required input is the file: phenotype_annotation.tab

try:
	hpofile = sys.argv[1]
	query = sys.argv[2:]
except IOError as (errno,strerror):
	print "usage: omim_to_hpo.py phenotype_annotation.tab omim query space separated"
	
search_obj = omim_api.Search()
results = search_obj.omim_by_search(query)

for res in results:
	print res

