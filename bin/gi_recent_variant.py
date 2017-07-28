#!/usr/bin/env python
import gi_util
import sys

# pull out all variants of a given class since inputted number of days ago

user = "gigpad_clinical"
password = "g2J$3KHU"
host = "racclusr2.dipr.partners.org"
port = 1521
service = "gpadprod.pcpgm.partners.org"
db = host+":"+str(port)+"/"+service


try:
	num_days = sys.argv[1]
except:
	print "usage: gi_recent_class.py num_days_to_go_back"
	exit();

db_obj = gi_util.CMS_DB(db=db,user=user,password=password)


# get recent missense variants
recent = db_obj.ask(db_obj.recent_variant_query(num_days))

genes_and_names = [entry[1]+"\t"+entry[2] for entry in recent]

print "\n".join(genes_and_names)


exit();
