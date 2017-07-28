#!/usr/bin/env python
import eutils_util as eu
import sys

url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

ids = sys.argv[1:]

eutil_obj = eu.Eutils(url)

description = eutil_obj.summary_by_entrez(ids)

print str(description)

