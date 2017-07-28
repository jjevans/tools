#!/usr/bin/env python
import re
import sys
import va_annotate
import va_excel
import va_process

# take alamut output and create a Variant Assessment excel sheet

# lmm test tab will have dummy data
tests = [("dummy_test","dummy_transcript")]

try:
	conf = sys.argv[1]
	alamutfile = sys.argv[2]
except:
	print "usage: alamut_to_excel.py variant_assessment_config_yaml alamut_output_tbl_file"
	exit()

settings = va_process.Configure(config=conf).settings
vaa_obj = va_annotate.VA_Alamut() #alamut parser

# read in alamut output
with open(alamutfile) as handle:
	alamut_lines = handle.readlines()
		
# dict of variants and their output lines
alamut_colnames,alamut_variants = vaa_obj.process_output(alamut_lines)


### produce workbooks
# create workbook for each variant
for av in alamut_variants:
							
	# excel workbook filename
	# variant identifier with ".xls" extension.
	# a carrot (">") in id is changed to "_to_"
	wbname = re.sub(">","_to_",av)+"."+"test"+".xls"
	wbpath = wbname # writes to cwd


	# add excel file name to the variant dict, 
	# overwrites, but duplicate anyways
	idgene,iddnac = av.split("_",1) # identifier genename_dnachange
	#variants[idgene][iddnac]["excel"] = wbname

			
	# excel files
	pop_args = { "filename":wbpath,\
				"template":settings["Project"]["files"]["excel_template"],\
				"fields":settings["Project"]["files"]["field_lookup"],\
				"colnames":alamut_colnames,\
				"format":settings["Excel"]}

	# build table, create workbook
	pop_obj = va_excel.Populate(**pop_args)
	
	pop_obj.variant_book(filename=wbpath,tests=tests,results=alamut_variants[av])
	
exit()
