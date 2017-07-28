#!/usr/bin/env python
import omim_api
import sys

# query omim for the genes related to a phenotype

apiKey = "E0DE3A210B372808F7F7CCFA88499D0C4C8A6A60" #2013
apiKey = "2EF035ECBD2E73BA368BECD371EA3E9E35D84034" #new for 2014
url = "http://api.omim.org/api"

try:
	omim = sys.argv[1]
except:
	print "usage: omim_gene_by_pheno.py omim_phenotype_number"
	exit(0)

omim_obj = omim_api.Pheno(apiKey,url)

symbols = omim_obj.get_genes(omim)

if symbols is None:
	print omim+"\tNone"
elif symbols == "Error":
	print "Error in retrieval from OMIM!"
else:
	for sym in symbols:
		print omim+"\t"+sym
