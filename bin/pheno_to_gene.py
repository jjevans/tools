#!/usr/bin/env python

import sys

''' break up hpo file "diseases_to_genes_to_phenotypes.txt" from 
	human-phenotype-ontology.org.  creates a data structure as a 
	dictionary with phenotype as key and lists of genes,
	outputs phenotype and a comma sep string of gene symbols '''
	
def dup_exist(lst,id):
	# checks through a list of tuples (first element, phenotype) to see 
	# if id is already represented
	
	for elem in lst:
		
		if elem == id:
			return True
			
	return False




try:
	hpofile = sys.argv[1]
except IOError as (errno,strerr):
	print "pheno_to_gene.py disease_to_genes_to_phenotypes.txt"
	
phenos = dict()

with open(hpofile) as handle:
	
	for line in handle.readlines():
		
		if line.startswith("#"):
			continue
		else:
			(disease,phenotype,description,symbol,entrez) = line.split("\t")

			# phenos dictionary, key is phenotype and value is a list gene symbols
			if not phenos.has_key(phenotype):
				phenos[phenotype] = list()
				
			if not dup_exist(phenos[phenotype],symbol):
				phenos[phenotype].append(symbol)

# print out omim id and a comma separated list of phenotypes for that omim
for pheno in phenos.keys():
	print pheno + "\t" + ",".join(phenos[pheno])
