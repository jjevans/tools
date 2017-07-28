#!/usr/bin/env python
import omim_api
import sys

apiKey = "E0DE3A210B372808F7F7CCFA88499D0C4C8A6A60" #2013
apiKey = "2EF035ECBD2E73BA368BECD371EA3E9E35D84034" #new for 2014
url = "http://api.omim.org/api"

#omim = 160760

try:
	omim = sys.argv[1]
#except IOError as (errno,strerror):
except:
	print "usage: omim_sym_by_num.py omim_number"
	exit(0)
	
omim_obj = omim_api.Use(apiKey,url)
symbols = omim_obj.sym_by_omim(omim)

for symbol in symbols:
	symlst = symbol.split(", ")
	
	for elem in symlst:
		print elem
		

exit(0)

