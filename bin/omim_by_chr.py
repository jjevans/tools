#!/usr/bin/env python
import omim_api
import sys

apiKey = "E0DE3A210B372808F7F7CCFA88499D0C4C8A6A60" #2013
apiKey = "2EF035ECBD2E73BA368BECD371EA3E9E35D84034" #new for 2014
url = "http://api.omim.org/api"
	
omim_obj = omim_api.Use(apiKey,url)
omims = omim_obj.omim_by_chr(chr)

for omim in omims:
	print omim
