#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import sys

#MUST BE WITHING THE PARTNERS NETWORK TO THE THAT SPECIFIC URL
#get current release of HGMD Pro database files 
# and supplements.  Goes to biobase, authenticates, 
# and retrieves all files in their current release.
url = "https://biobase-download.partners.org/cgi-bin/portal/login.cgi"
login_form_id = "login_form"


#user = "mlebo"
#passwd = "Genome65LND"

try:
	user = sys.argv[1]
	passwd = sys.argv[2]
except:
	print "usage: dl_hgmd.py username password"
	exit(0)

req = requests.get(url,auth=(user,passwd))

print req.text







"""
br = mech.Browser()

br.set_handle_robots(False)# ignore robots
br.set_handle_refresh(False)# can sometimes hang without this
br.open(url)

#br.select_form("login_form")

#login_frm = br.forms[0]
#login_pg = br.open(url)
#login_html = login_pg.read()
for form in br.forms():
	print form


#print str(login_frm)
"""

exit(0)