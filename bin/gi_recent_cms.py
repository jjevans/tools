#!/usr/bin/env python
import gi_util
import sys

# pull out all variants in cms processed the specified number of days ago
#  prints either table (default) or vcf format to stdout
#arg is the number of days to go back into cms (required)

user = "gigpad_clinical"
password = "g2J$3KHU"
host = "racclusr2.dipr.partners.org"
port = 1521
service = "gpadprod.pcpgm.partners.org"
db = host+":"+str(port)+"/"+service

wsuser = "lmm"
wspassword = "x377BLCi"
wsurl = "https://geneinsight-lmm-ws.partners.org/services/Variant?wsdl"


try:
	num_days = sys.argv[1]
except:
	print "usage: gi_recent_class.py num_days_to_go_back_in_cms"
	exit();

db_obj = gi_util.CMS_DB(db=db,user=user,password=password)
ws_obj = gi_util.GI_Variant(wsuser=wsuser,wspass=wspassword,wsurl=wsurl)


# get recent missense variants
recent = db_obj.ask(db_obj.recent_variant_query(num_days))

vids = list()
for identifier,gene,name,exon in recent:
	entries = ws_obj.geneAndVariant(gene,name)
	
	for entry in entries:
		print str(identifier)+"\t"+gene+"\t"+name+"\t"+entry["category"]

	'''
	try:# find category of first entry
		"""
		if entries[0]["category"] == category:
			print str(entries[0])+" yes"+identifier
			vids.append(identifier)
		"""
		print name+"\t"+entries[0]["category"]+"\n"
			
	except:# no entry or no category
		pass
	'''
"""
print str(vids)+"\n\n\n"
print str(recent)+"\n\n\n"
if len(vids) > 0:
	variants = db_obj.ask(db_obj.variant_detail_query(vids))
else:
	print str(None)
"""
"""
with open(vcf) as handle:
	handle.write("##fileformat=VCFv4.1\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
	
	for variant in variants:
		print str(variant)

		genename = variant[0]
		dnachange = variant[2]
		coolid = genename+"_"+dnachange
		
		chrom,coords = variant[4].split(":")
		
		position = coords.split("-")[0]
		
		vcf_line = chrom+"\t"+"\t"+position+"\t"+coolid+"\t"+variant[5]+"\t"+variant[6]+"\t"*3
		handle.write(vcf_line)
"""

exit();
