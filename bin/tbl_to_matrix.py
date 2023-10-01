#!/usr/bin/env python
import sys

rownames = list()
colnames = list()
mat = list()
matfreq = list()#2nd matrix

try:
	to_matrixify = sys.argv[1]
except:
	sys.stderr.write("usage: tbl_to_matrix.py table_to_matrixify\n")
	exit(1)
	
with open(to_matrixify) as handle:

	#first pass to get unique names
	for line in handle.readlines():
		col = line.rstrip().split("\t")
		vid = ":".join(col[1:5]);	
		#add col and/or row if not exists
		try:
			colnames.index(vid)
		except:
			colnames.append(vid)
			
		try:
			rownames.index(col[0])
		except:
			rownames.append(col[0])
	
	#init matrix 
	for rowname in rownames:
		mat.append(["NA"]*len(colnames))
	
	#2nd pass, populate matrix
	handle.seek(0,0)
	for line in handle.readlines():
		col = line.rstrip().split("\t")
		vid = ":".join(col[1:5]);
		colnum = colnames.index(vid)
		rownum = rownames.index(col[0])

		mat[rownum][colnum] = col[-1]
		
#print mat to stdout, matfreq to stderr
#header
print "samples\t" + "\t".join(colnames)
	
for i, rowname in enumerate(rownames):
	print rowname + "\t" + "\t".join(mat[i])
		
	
exit()
