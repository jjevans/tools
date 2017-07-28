#!/usr/bin/env python
import hgvs_bfx
import sys

#jje16, msl34	04012015
#convert a variant gdot hgvs nomenclature to a vcf entry

#input is a list of variants in hgvs nomenclature (NM_001:c.175C>T), 
# a refgene formatted transcripts file (UCSC goldenpath refGene.txt)
# and a reference fasta file (genome)
try:
	ref_fa = sys.argv[1]
	ref_tr = sys.argv[2]
except:
	sys.stderr.write("usage: hgvs_to_vcf.py hgvs_variants (nc:g./nm:c.)\n") refGene.txt_file reference_fasta_file\n")
	exit()

hgvs_obj = hgvs_bfx.Hgvs(ref_fa=ref_fa,ref_tr=ref_tr)

exit()
