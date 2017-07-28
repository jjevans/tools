#!/usr/bin/env python

import path_graph
import shutil
import sys

try:
	outfile = sys.argv[1]
	db = sys.argv[2]
	pathway = " ".join(sys.argv[3:])
	
except IOError:
	print "usage: pathway_graph.py path_db path_name output_file"

graph_obj = path_graph.Use()

graph = graph_obj.graph_by_name(db,pathway)

graph_obj.save_xgmml(graph,outfile)

# BioNet saves output xgmml as inputted filebase and adds ".xgmml" to it 
# as an extension.  To cooperate with Galaxy, need to mv the file.xgmml to 
# the filename passed in as outfile

try:
	shutil.move(outfile+".xgmml",outfile)
except IOError:
	print "cannot rename output file by truncating xgmml extension"
	
