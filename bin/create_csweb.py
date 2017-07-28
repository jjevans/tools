#!/usr/bin/env python

import csweb_api
import csweb_page

import os
import re
import shutil
import sys

# create the network for cs web in either the network model or 
# XGMML formats from a file.  mako template, yaml config, 
# filename for output, directory to store supporting files

path = os.path.dirname(__file__)

# supporting files
js1 = path+"/"+"json2.js"
js2 = path+"/"+"AC_OETags.js"
js3 = path+"/"+"cytoscapeweb.js"
swf1 = path+"/"+"CytoscapeWeb.swf"
plate = path+"/"+"csweb_plate.mako"

#js1 = "json2.js"
#js2 = "AC_OETags.js"
#js3 = "cytoscapeweb.js"
#swf1 = "CytoscapeWeb.swf"
#plate = "csweb_plate.mako"

try:
	netfile = sys.argv[1]
	config = path+"/"+sys.argv[2]
	#config = sys.argv[2]
	outfile = sys.argv[3]
	extra_files_dir = sys.argv[4]
	
#except IOError as (errno, strerror):
except:
	print "usage: create_csweb.py network template config outfile extra_files_dir"
        exit(0)

#### read and structure attribute configs
with open(config) as handle:
	conf_str = handle.read()
			
csw_set = csweb_api.Settings(conf_str)
annos = csw_set.anno
styles = csw_set.style

#### merge group styles with other general visual styles
## unimplemented
#csw_sty = csweb_api.Styles(styles)
#merge = csw_sty.merge_sty()

#### read in network in gml, xgmml, or as adjacency pairs
with open(netfile) as handle:
	content = handle.read()

#### create network if needs to be created otherwise just return gml/xgmml
csw_net = csweb_api.Nets(content)
network = csw_net.net

#### assemble data
csw_page = csweb_page.Page_Gen(plate,network,styles,annos)
webpage = csw_page.html

#### get the basename of the file from the output file path and produce 
## the extra files directory (fix for Galaxy).
## help from Brad Chapman to piece together the output file directory 
#print outfile
base_dir, file_base = os.path.split(outfile)
print base_dir+"#"+file_base
print os.path.splitext(file_base)[0]
#extra_files_dir = os.path.join(base_dir, "{}_files".format(os.path.splitext(file_base)[0]))
extra_files_dir = base_dir+"/"+os.path.splitext(file_base)[0]+"_files"

#### make supporting files directory, copy in files
if not os.path.exists(extra_files_dir):
	os.mkdir(extra_files_dir)

#### copy supporting Cytoscape Web files
#### json.js, ac_eotags.js, and cytoscapeweb.js, CytoscapeWeb.swf
shutil.copy(js1,extra_files_dir+"/")
shutil.copy(js2,extra_files_dir+"/")
shutil.copy(js3,extra_files_dir+"/")
shutil.copy(swf1,extra_files_dir+"/")

#print extra_files_dir

#### write page to output
with open(outfile,'w') as handle:
	handle.write(webpage)

exit(0)
