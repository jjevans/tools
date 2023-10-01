#!/usr/bin/env python
import sys
import st

#get basepair resolution coverage, mapping quality and flag stats from bam over bed regions
#jje 03022021

try:
    bamfile = sys.argv[1]
    bedfile = sys.argv[2]
except:
    sys.stderr.write("usage: st_mq_bpres.py align.bam region.bed\n")
    exit(1)

st_obj = st.Bam(bamfile=bamfile, bedfile=bedfile)
colnames, outrows = st_obj.region_stats()

if len(outrows) > 0:
    sys.stdout.write("\t".join(colnames)+"\n")        
    for outrow in outrows:
        sys.stdout.write("\t".join(outrow)+"\n")

exit()
