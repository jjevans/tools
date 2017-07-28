#!/usr/bin/env python
import bm_util
import sys

url="http://www.biomart.org/biomart/martservice"

# example data, ENSG00000184702,ENSG00000125354,ENSG00000122545
try:
	ids = sys.argv[1]
except:
	print "bm_ensg_exon.py ensembl_ids_by_comma\n\ttry: ENSG00000184702,ENSG00000125354,ENSG00000122545"
	exit()

bm_obj = bm_util.ENSG(url=url)

restbl = bm_obj.exon_by_id(ids,header=True)

print restbl,

exit()
