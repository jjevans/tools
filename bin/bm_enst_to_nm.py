#!/usr/bin/env python
import bm_util
import sys

#__UNFINISHED__
#convert an ensembl transcript id (ENST) 
# to a refseq transcript id

try:
	id = sys.argv[1]
except:
	print "usage: bm_enst_to_nm.py ensembl_transcript_id"
	exit(0)
	
convert_obj = bm_util.Convert()

response = convert_obj.enst_to_nm(id)

print response

exit(0)
