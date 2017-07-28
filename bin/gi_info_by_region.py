#!/usr/bin/env python
import gi_util
import sys

# get the GeneInsight information for a region's genomic coordinates.
# input is a chromosome, start position, end position

# test values
chrom=13
start=20763342
end=20763342

wsurl="https://geneinsight-lmm-ws.partners.org/services/GenomeBuildMapping?wsdl"
wsuser="lmm"
wspass="x377BLCi"

try:
	chrom = sys.argv[1]
	start = sys.argv[2]
	end = sys.argv[3]
except:
	print "NO REGION COORDINATES PROVIDED! Using test region!\nusage: gi_info_by_region.py chromosome start_position end_position\n"

print "####\nregion: "+str(chrom)+":"+str(start)+"-"+str(end)+"\n####"

gi_obj = gi_util.GI_GenomeBuildMapping(wsurl=wsurl,wsuser=wsuser,wspass=wspass)
annos = gi_obj.region_info(chrom,start,end)

if annos is not None:
	for i,anno in enumerate(annos):
		print "entry: "+str(i)
		print str(anno)
		#for key in anno:
			#print key[0]+": "+str(key[1])

		print "####"
else:
	print "No info found."

exit(0)
