#!/usr/bin/env python
import GOstats_Process
import GOstats_R
import gPro
import os
import shutil
import sys

''' run GOstats on multiple gene lists and merge the results of terms 
	found in the lists concomitantly. '''

# input is the output file to create heatmap as, the number of gene sets 
# needed to represent a term for it to be reported, a GOstats p-value cutoff, 
# and a series of files of lists of ids in text format.  
# Minimum number of files is 1 with no upper lim.
# uses g:Profiler, g:Convert to convert all ids to entrez gene for GOstats
# some ids will drop out from conversion back and forth

# argv
# 1 output file provided by Galaxy
# 2 minimum num gene lists having a certain GO term in order to report it
# 3 ontology "BP","MF","CC"
# 4 p-value cutoff for GOstats
# 5- 1 or more gene lists to put in the heatmap

# file to print heatmap to, Galaxy provided file to move outfile to, file type
filetype = "pdf"
galfile = sys.argv[1]
outfile = galfile+"."+filetype

# column from GOstats summary table having the value to put in heatmap 
# the GO term id is always in column 0, column 6 has GO term description
# take the -log2 value if column is a string ("1" vs 1), min_set is the min 
# num gene lists required having a given term to be reported
hot_col = "1" #pvalue, string so -log2 it
null_val = 0
min_set = sys.argv[2]

# GOstats parameters, keep pcut high so more entries overlap with gene lists,
# p-value cutoff inputted by user, type of ontology ("BP","MF","CC") user input
ont = sys.argv[3]
db = "org.Hs.eg" #human
pcut = sys.argv[4]

# g:Profiler object, GOstats heatmap initialized 
gpro_obj = gPro.Convert_ID()
merge_obj = GOstats_Process.Merge()
hm_obj = GOstats_Process.Heatmap()

# keep a list of dictionaries one for each gene set, produce dict of lists 
# by term as key, filebases is ultimately the colnames in heatmap
term_dicts = list()
filebases = list()

# each file, convert ids, run GOstats,
# starts from argv[5]
for filepath in sys.argv[5:]:
	filebases.append(os.path.basename(filepath))
	
	with open(filepath) as handle:
		ids = handle.read()
	
	# Convert ids to Entrez Gene Accessions
	# g:Convert takes a newline delim string of ids
	# comes back with newline delimited string though GOstats uses a list
	entrez_ids = gpro_obj.to_entrez(ids).splitlines() #uses http
	
	# GOstats
	go_obj = GOstats_R.Use(entrez_ids,ont=ont,db=db,pcut=pcut)
	go_res = go_obj.run()
	smry_tbl = go_res.summary() 
	
	# pull values from gostats summary, requires gostats summary, and an 
	# hot_col is the column of GOstats summary to use in the heatmap 
	# (default pvalue), returns a dictionary of tuples with GO term as key 
	# and the value is the value to put in the heatmap
	term_vals = merge_obj.term_by_val(smry_tbl,hot_col)
	
	term_dicts.append(term_vals)

# organize a 2-D array within a dictionary.  GO term as key, list of 
# values (pvals) as values, null_val is the value that should be used if 
# there is no go record for that set (place holder)
py_mat = merge_obj.term_merge(term_dicts,null_val)

# convert to r matrix, filebases is the text wanted for the 
# equivalent of colnames in R, min_overlap limits results to GO terms 
# existing in that many sets to be shown. check inputted min_set and 
# reset to the number of sets provided if user value > num sets provided
#print str(min_set)+"\t"+str(len(term_dicts))
#if min_set > len(term_dicts):
#	min_set = len(term_dicts)
#print str(min_set)+"wow"
ol_mat = merge_obj.min_overlap(py_mat,min_set,null_val)
r_mat = merge_obj.build_mat(ol_mat,filebases) #uses R

# produce heatmap to outfile, move to the filename provided by Galaxy
try:
	hm_obj.pretty_hm(r_mat,outfile) #uses R
	shutil.move(outfile,galfile)
except:
	print "No results found.  Try a lower stringency."
