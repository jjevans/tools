#!/usr/bin/env python

import omim_api
import sys

# do a text search at omim to get the associated terms
apiKey = "E0DE3A210B372808F7F7CCFA88499D0C4C8A6A60" #2013
apiKey = "2EF035ECBD2E73BA368BECD371EA3E9E35D84034" #new for 2014
url = "http://api.omim.org/api"

try:
	terms = " ".join(sys.argv[1:])
	sys.argv[1] == None # raise error if no arguments
except:
	print "omim_by_search.py space_separated_search_terms"
	sys.exit(0)
	
if terms == "":
	print "No terms provided"
	
omim_obj = omim_api.Search(apiKey,url)

response = "\n".join(omim_obj.omim_by_search(terms))

print response

