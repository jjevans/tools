#!/usr/bin/env python
import sys
import templateCreator
import xlwt

# jje 09302013, used to produce an excel workbook serving as a template 
# which will be populated by the NVA tool

try:
	template_file = sys.argv[1]
except:
	print "usage: create_template.py template_output_excel_filename"
	exit(0)
	
sheet_name = "template"

book = xlwt.Workbook()

templateCreator.populateFormatWorksheet(sheet_name,book)

book.save(template_file)

exit(0)
