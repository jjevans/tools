#!/usr/bin/env python

import sys

try:
	termfile = sys.argv[1]
	outfile = sys.argv[2]
except:
	print "usage: ReviGO.py file_of_GO_terms output_file"
	
with open(termfile) as handle:
	terms = handle.read()

html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><title>link to REVIGO</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body><form action="http://revigo.irb.hr/" method="post"><textarea name="inputGoList" rows="50" cols="25">'''+terms+'''</textarea><input type="submit" name="startRevigo" value="Go to Revigo" /></form></body></html>'''

with open(outfile,'w') as handle:
	handle.write(html)
	
