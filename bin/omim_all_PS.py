#!/usr/bin/env python
import omim_util

# html page of phenotypicSeries list of all series entries
# The webpage link is for all the phenotypicSeries titles (table 
# of omim ids each as a representative of a PS).
# Must be the "title" page with one main table of omim description 
# and the omim id of the representative entry of the omim series.
# It is not the page with a table of ids for each series!!!
# east coast mirror (default) and main page
# http://us-east.omim.org/phenotypicSeriesTitle/all
# http://www.omim.org/phenotypicSeriesTitle/all
ps_page = "http://us-east.omim.org/phenotypicSeriesTitle/all"

# get a list of all phenotypicSeries entries
# screenscrapes the ps title page for all phenotypicseries 
# entries and follows links to get all subdiseases for each PS
# outputs a table to stdout with main series representative 
# entry pheno id and omim sub member pheno id
# note: there may be duplicate rows of series id<tab>member id as 
# one omim id may have two different descriptions and have two different 
# rows in the table of each phenotypic series!
omim_obj = omim_util.Series(ps_page)

links = omim_obj.series_links() # link to each series
all = omim_obj.all_info(links)


# pheno series dict
for ps in all:
	
	# None is a bad link or no info
	if all[ps] is not None:
		
		# go through all phenos in series list
		for sub in all[ps]:
		
			# sub values: None caused by bad link
			#print ps+"\t"+sub[3]+"\t"+sub[1]
			if sub[3] == "268000":
				print str(sub)

exit(0)
