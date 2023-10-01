#!/usr/bin/env python
import urllib
import requests as req
import sys
import json

#jje 07272020
#use mutalyzer to convert HGVS nomenclature for a variant into VCF format

valid_url = "https://mutalyzer.nl/json/checkSyntax"
mtlyzr_url = "https://mutalyzer.nl/json/runMutalyzer"


try:
        hgvs = sys.argv[1]
except:
        sys.stderr.write("usage: hgvs_to_vcf.py NM00:c.11delC\n")
        exit(1)

param = {"variant": hgvs}

res = req.get(mtlyzr_url, params=param)

sys.stderr.write("INFO: url="+res.url+"\n")

print(json.dumps(json.loads(res.text), indent=4, sort_keys=True))


exit()

