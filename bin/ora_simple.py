#!/usr/bin/env python
import sys
import ora_util

#generic oracle query tool
qry = "describe pcrseq_templates"

#db creds
db = "racclusr2.dipr.partners.org:1521/GPADPROD"
user = "chr12"
passwd = "raju"

# db is in the form host:port/service_id

print user+" "+passwd+" "+db

ora_obj = ora_util.Query(db,user,passwd)

res = ora_obj.ask(qry)
print "res\t"+str(res)

exit()

