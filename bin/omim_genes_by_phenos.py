#!/usr/bin/env python
import omim_api
import sys

# query omim for the genes related to a phenotype

apiKey = "E0DE3A210B372808F7F7CCFA88499D0C4C8A6A60" #2013
apiKey = "2EF035ECBD2E73BA368BECD371EA3E9E35D84034" #new for 2014
url = "http://api.omim.org/api"

try:
	file = sys.argv[1]
except:
	print "usage: omim_genes_by_phenos.py file_of_omim_phenotype_numbers"
	exit(0)
	
omim_obj = omim_api.Pheno(apiKey,url)

with open(file) as handle:
		
	for pheno in handle.readlines():	
		symbols = omim_obj.get_genes(pheno)

	if symbols is None:
		print pheno+"\tNone"
	elif symbols == "Error":
		print "Error in retrieval from OMIM!"
	else:
		for sym in symbols:
			print pheno+"\t"+sym
