#!/usr/bin/env python
from pymongo import MongoClient
import sys

#get collections of mongo CR db
#jje, jw	11122015
host = ["172.16.10.55","172.16.20.55","172.16.20.56"]
port = "27017"
db = "CR"

mongo = MongoClient(host,int(port))
m_db = mongo[db]

i0 = {'jason':'evans', 'fun':True, 'living':'large'}
i1 = {'saurabh':'tuli', 'fun':False, 'living':'small'}
i2 = {'dan':'watson', 'fun':True, 'living':'normal'}

m_collect = m_db['evs_tmp_0']
info = [i0, i1, i2]
info_dict = {'test':True, 'works':'hopefully', 'information':info}

m_collect.save(info_dict)

exit()
