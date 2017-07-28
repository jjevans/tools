#!/usr/bin/env python
from bs4 import BeautifulSoup
import mechanize as mech
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


br = mech.Browser()

br.set_handle_robots(False)# ignore robots
#br.set_handle_refresh(False)# can sometimes hang without this
login_page = br.open(url)

bs = BeautifulSoup(login_page.read())

form_id = bs.find(class="ta1")

print form_id
#login_form = None

#for form in br.forms():
#	print str(form.attrs)
"""
	if form.attrs["id"] == "login_form":
		login_form = form
	

if not login_form:
	raise Exception("cannot identify login form!")
else:
	print login_form.attrs["id"]



#br.select_form(nr=0)
#br.select_form(name="login_form")


#br.form["login"]=user
#br.form["password"]=passwd
#req = br.submit()
#print str(req)
"""

exit(0)