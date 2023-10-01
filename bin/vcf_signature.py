#!/usr/bin/env python
import sys
import subprocess
import dxpy

#make identity string from vcf and bedfile of positions.  any '.', multiallelic, indel equates to 'N', otherwise its genotype
#jje 12092019
default_wildcard = "N"

try:
	vcffile = sys.argv[1]
	bedfile = sys.argv[2]
	try:
		outfile = sys.argv[3]
	except:
		outfile = None
	try:
		wildcard = sys.argv[4]
	except:
		wildcard = default_wildcard
except:
	message = "usage: vcf_id_str.py vcf_file bed_file_of_positions outfile(optional, default: stdout) wildcard_character(optional, default=" + str(default_wildcard) + ")\n"

	sys.stderr.write(message)
	exit(1)

#use bcftools view to pull out all sites from bed file
cmd = "bcftools view -T " + bedfile + " " + vcffile

sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

out, err = sp.communicate()

if sp.returncode != 0:#error
	message = "ERROR: non-zero exit status returned: " + str(sp.returncode) + "\nERROR: message returned: " + str(err) + "\n"
	raise Exception(message)

identity = str()

lines = out.split("\n")
for line in lines:
	if not line.startswith("#") and line != "":
		cols = line.rstrip().split("\t")
		alt = cols[4]

		if len(alt) > 1:
			identity += wildcard
		elif alt == ".":#add ref
			identity += cols[3]
		else:
			identity += alt

if outfile is not None:
	with open(outfile, 'w') as handle:
		handle.write(identity)
else:
	sys.stdout.write(identity)

exit()
		
