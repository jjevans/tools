#!/usr/bin/env python
import omim_api
import sys

apiKey = "E0DE3A210B372808F7F7CCFA88499D0C4C8A6A60" #2013
apiKey = "2EF035ECBD2E73BA368BECD371EA3E9E35D84034" #new for 2014
url = "http://api.omim.org/api"

try:
	omim = sys.argv[1]
except IOError as (errno,strerror):
	print "usage: omim_variant_by_num.py omim_number"
	
omim_obj = omim_api.Use(apiKey,url)
variants = omim_obj.variant_by_omim(omim)

print variants
