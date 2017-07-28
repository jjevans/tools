#!/usr/bin/env python

import metamap_util
import sys

cuid_kw = "mapping"

try:
	phrase = " ".join(sys.argv[1:])
except IOError as (errno,strerr):
	print "cuid_query.py query_string"

mm_obj = metamap_util.Query()

mm_obj.ask(phrase)

if getattr(mm_obj,cuid_kw) is not None:

	for value in getattr(mm_obj,cuid_kw):
		print value["cuid"] + "\t" + value["desc"] + "\t" + value["score"]
