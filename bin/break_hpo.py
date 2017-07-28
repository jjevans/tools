import hpo #requires tbl_util.py
import sys

# input is a file with hpo id<tab>pheno name<tab>entrez<tab>gene symbol<nl>

try:
	hpofile = sys.argv[1]
except IOError as (errno,strerr):
	print "usage: break_hpo.py hpo_file"
	
hpo_obj = hpo.Organize(hpofile)
content = hpo_obj.org_by_pheno()

for pheno in content:
	for entry in content[pheno]:
		print pheno + "\t" + str(entry)
