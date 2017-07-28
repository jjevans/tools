#!/usr/bin/env python
import anno_exac
import sys

#parse exac data to format for SnpEff for upload to db
#jje16	04202015
#partners personalized medicine, biofx

#input is an exac vcf (raw, direct download from BROAD)
#outputs uploader formatted vcf on stdout
try:
	vcf = sys.argv[1]

	try:
		tags = sys.argv[2].split(',')
	except:
		tags = None
except:
	sys.stderr.write('usage: exac_to_upldr.py raw_exac_vcf desired_tags(default all, comma separated)\n')
	exit(1)
	
exac = anno_exac.Vcf(vcf)


#exac.parse()
'''
for rec in exac.reader:
	print rec.INFO
'''
print exac.reader.next().INFO

#exac_obj.parse()
#print '\n'.join(exac_obj.to_upldr())

exit()
