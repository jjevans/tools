#!/usr/bin/env python
import re
import sys
import va_annotate
import va_excel
import yaml

# take alamut output and create a Variant Assessment excel sheet

# lmm test tab will have dummy data
tests = [("dummy_test","dummy_transcript")]

try:
	alamutfile = sys.argv[1]
	templatefile = sys.argv[2]
	fieldsfile = sys.argv[3]
except:
	print "usage: alamut_to_excel.py alamut_output_tbl_file nva_xls_template_file nva_xls_fields_file"
	exit()

# excel formats (from nva config)
form_yml = '''
    format:
        definitions:
            &HEADER header: "pattern: pattern solid, fore_colour lavender;font: colour black, bold True;"
            &HYPERLINK hyperlink: "font: colour blue, underline True;"
        locations: # string of row and column separated by comma
            tests:
                0,0: *HEADER
                0,1: *HEADER
            transcripts:
                0,0: *HEADER
                0,1: *HEADER
                0,2: *HEADER
                0,3: *HEADER
                71,0: *HEADER
                71,1: *HEADER
                71,2: *HEADER
                71,3: *HEADER
                80,0: *HEADER
                80,1: *HEADER
                80,2: *HEADER
                80,3: *HEADER
                90,0: *HEADER
                90,1: *HEADER
                90,2: *HEADER
                90,3: *HEADER
                70,3: *HYPERLINK
    column_widths: #array of column number and column width
        tests:
            - [0,6400]
            - [1,6400]
        transcripts:
            - [0,15360]
            - [1,7424]
            - [2,7680]
            - [3,48384]'''

format = yaml.load(form_yml)


#settings = va_process.Configure(config=conf).settings
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
				"template":templatefile,\
				"fields":fieldsfile,\
				"colnames":alamut_colnames,\
				"format":format}

	# build table, create workbook
	pop_obj = va_excel.Populate(**pop_args)
	
	pop_obj.variant_book(filename=wbpath,tests=tests,results=alamut_variants[av])
	
exit()
