#!/usr/bin/env python
import MySQLdb as mysql
import sys

test_coords = ((1,156836733,156836734),(9,71650816,71650816),(1,100376383,100376384))

#query hgmd database for variant information based on 
# a variant chromosomal location
#Input is a vcf file

#query
query = "select chromosome,\
				startcoord,\
				endcoord,\
				acc_num,\
				hgvs,\
				base,\
				disease,\
				gene,\
				chrom,\
				genename,\
				gdbid,\
				omimid,\
				amino,\
				deletion,\
				insertion,\
				codon,\
				codonaff,\
				descr,\
				hgvs,\
				hgvsall,\
				dbsnp,\
				tag,\
				author,\
				fullname,\
				allname,\
				vol,\
				page,\
				year,\
				pmid,\
				reftag,\
				comments,\
				acc_num,\
				new_date,\
				base \
			from allmut \
			where chromosome=%s \
				and startcoord=%s \
				and endcoord=%s"
				

try:
	vcf = sys.argv[1]
	db = sys.argv[2]
	user = sys.argv[3]
	password = sys.argv[4]
	host = sys.argv[5]
except:
	print "usage hgmd_by_coord.py vcf_file db (hgmd2) username (wgs_user) password (Pju7ogJQ) host (hpcdb.research.partners.org)"
	exit(0)

db_obj = mysql.connect(db=db,user=user,passwd=password,host=host)
curs = db_obj.cursor()

with open(vcf) as handle:
	for coord in test_coords:
		curs.execute(query,(coord[0],coord[1],coord[1]))

		for res in curs.fetchall():
			for elem in res:
				print str(elem)+"\t",
			print

exit(0)
