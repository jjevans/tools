#!/usr/bin/env python
import sys
import va_process


####
# Jason Evans
# Matt Lebo
# Partners Personalized Medicine
# Partners Healthcare
####

# queries cms and geneinsight for variants with certain criteria.  
# see config for nva_conf.yml
####

# argument is configuration file. see cms_conf.yml (NVA conf nva_conf.yml)
# prints variants in vcf to stdout
####
try:
	config = sys.argv[1]
except:
	print "usage: va_cms.py config_file(see nva_conf.yml)"
	exit()


process_obj = va_process.QueryCMS(config)

vcf_lines = process_obj.days_ago()

for line in vcf_lines:
	print line

exit()

