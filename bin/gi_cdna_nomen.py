#!/usr/bin/env python
import argparse
import gi_util

###!!!NOT FINISHED!!!

#pull out the cdna cooordinates (nomenclature) 
# from GeneInsight Variant web service
#Input is a vcf file

#default wsdl
default_wsdl = "https://geneinsight-lmm-ws.partners.org/services/Variant?wsdl"
default_user = "lmm"
default_pass = "x377BLCi"

default_gbm_wsdl = "https://geneinsight-lmm-ws.partners.org/services/GenomeBuildMapping?wsdl"

parser = argparse.ArgumentParser()
parser.add_argument("vcf")
parser.add_argument("-w","--wsdl",help="GeneInsight Variant WSDL",default=default_gbm_wsdl)
parser.add_argument("-u","--user",help="GeneInsight username",default=default_user)
parser.add_argument("-p","--password",help="GeneInsight password",default=default_pass)

args = parser.parse_args()

#connect to geneinsight
#gi_variant = gi_util.WS_Variant(wsurl=args.wsdl,wsuser=args.user,wspass=args.password)
gi_gbm = gi_util.GI_GenomeBuildMapping(wsurl=args.wsdl,wsuser=args.user,wspass=args.password)

with open(args.vcf) as handle:

	for line in handle.readlines():
		if not line.startswith("#"):
			mut = line.rstrip("\n").split("\t")
			print str(mut)
			#info = gi_gbm.region_info(str(mut[0]),str(mut[1]),str(int(mut[2]+1)))
			info = gi_gbm.region_info(str(mut[0]), str(mut[1]), str(int(mut[1])+1))
			print str(info)

exit(0)
