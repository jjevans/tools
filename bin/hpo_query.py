#!/usr/bin/env python
import MySQLdb as mysql
import sys

database = "hpo0"
username = "python"
hostname = "localhost"

try:
	query = " ".join(sys.argv[1:])
except:
	print "hpo_query.py seq_query"

db = mysql.connect(db=database,user=username,host=hostname)
curs = db.cursor()
curs.execute(query)

for ans in curs.fetchall():
	for col in ans:
		print str(col),
	print
