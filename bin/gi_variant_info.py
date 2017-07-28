#!/usr/bin/env python
import gi_util
import sys

#query geneinsight for all variant info 
# from inputted gene name and geneinsight 
# variant name (our lab)


#hard-coded gi web service credentials
wsuser = "lmm"
wspass = "x377BLCi"
wsurl = "https://geneinsight-lmm-ws.partners.org/services/Variant?wsdl"


try:
	gene = sys.argv[1]
	variant = sys.argv[2]
except:
	print "gi_variant_info.py gene_name variant_name\n\n*** MAKE SURE TO USE QUOTES IN VARIANT NAME (TRICKY CHARACTERS)\n\ntry the test case:\n    gene: SGCD\n    variant: \"717C>G\"\n\n"
	exit()
	

gi_obj = gi_util.GI_Variant(wsurl=wsurl,wsuser=wsuser,wspass=wspass)

response = gi_obj.geneAndVariant(gene=gene,name=variant)


print str(response)


exit()
