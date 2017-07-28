#!/usr/bin/env python
import argparse
import xml.etree.ElementTree as et
import requests as req

#from a chromosome, start, stop 
# get the human genomic sequence 
# by way of the ucsc das server
#outputs in fasta format 
# with id of "chr:start-stop"

#seq_by_coord.py 4 90637000 90651000

default_das = "http://genome.ucsc.edu/cgi-bin/das"
default_build = "hg19"

parser = argparse.ArgumentParser()
parser.add_argument("chromosome")
parser.add_argument("start")
parser.add_argument("stop")
parser.add_argument("--url",help="location of DAS server [ucsc das default]",default=default_das)
parser.add_argument("--build",help="genome build [hg19(default),hg38,etc]",default=default_build)
parser.add_argument("--id",help="id for fasta output [chr:start-stop(default)]")
parser.add_argument("--describe",help="put coordinate in fasta description",action="store_true")
args = parser.parse_args()

das_url = args.url+"/"+args.build+"/dna"

#chromosome, add chr if not supplied in arg
chr = str()
if not args.chromosome.startswith("chr"):
	chr = "chr"
chr += args.chromosome

#coordinate
segment = chr+":"+args.start+","+args.stop

#request
pars = {"segment":segment}
response = req.get(das_url,params=pars).text

#fasta id
id = segment.replace(",","-")
if args.id is not None:
	id = args.id

#print sequence
try:
	tree = et.fromstring(response)

	#seq has leading and trailing newline
	seq = tree.find(".//DNA").text

	#build fasta line
	faid = ">"+id
	
	if args.describe:
		faid += "\t"+segment.replace(",","-")

	#print
	#stripped newline then to add one in print
	print faid+seq.rstrip()

except:
	print "No sequence for: "+id

exit(0)
