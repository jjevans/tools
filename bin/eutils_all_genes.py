#!/usr/bin/env python
import eutils_util as eu
import MySQLdb as mysql

num_rec_per_query = 300

url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

db = "hpo_gene"
user = "python"
host = "localhost"

db_obj = mysql.connect(db=db,user=user,host=host)
curs = db_obj.cursor()

# get all genes from hpo_gene db (phenotype_to_gene.txt) and put
# entrez ids in the keys of a dict to efetch the descriptions
query = "select entrez,symbol from pheno_to_gene"

curs.execute(query)

genes = curs.fetchall()

entrezids = dict() #uniquify the dups
for gene in genes:
	entrezids[gene[0]] = gene[1]

ids = sorted(entrezids.keys())

# use eutils to fetch the gene descriptions 
eutil_obj = eu.Eutils(url)

num_entry = 0
query_ids = None
for id in ids:
	
	if num_entry % num_rec_per_query == 0 or num_entry == len(ids):
		if query_ids is not None:
			res = eutil_obj.desc_by_entrez(query_ids)
			print str(res)
		else:
			query_ids = list()
			
	query_ids.append(id)
	num_entry += 1
