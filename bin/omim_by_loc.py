#!/usr/bin/env python
import omim_api
import sys

#BROKEN, see omim_api.omim_by_location

apiKey = "E0DE3A210B372808F7F7CCFA88499D0C4C8A6A60" #2013
apiKey = "2EF035ECBD2E73BA368BECD371EA3E9E35D84034" #new for 2014
url = "http://api.omim.org/api"

try:
	chr = sys.argv[1]
	start = sys.argv[2]
	end = sys.argv[3]
#except IOError as (errno,strerror):
except:
	print "usage: omim_by_loc.py chromosome start end"
	exit(0)
	
omim_obj = omim_api.Use(apiKey,url)
omims = omim_obj.omim_by_location(chr,start,end)

for omim in omims:
	print omim

exit(0)

