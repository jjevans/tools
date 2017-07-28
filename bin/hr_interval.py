#!/usr/bin/env python
import requests
import sys

url = 'http://www.broadinstitute.org/mammals/haploreg/haploreg.php'

#submit genomic interval to HaploReg (BROAD)
#output response table
#ex: hr_interval.py chr12:500000-510000

try:
	interval = sys.argv[1]
except:
	print 'usage: hr_interval.py chr:start-stop'
	exit(1)


data = {'query':interval, 'output':'text' }

response = requests.post(url,data=data)

print response.text,

exit(0)
