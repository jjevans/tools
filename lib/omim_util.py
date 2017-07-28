import bs4
import requests as req
from urlparse import urlparse

# utilities to work with omim

class Series():

	def __init__(self,ps_page = "http://us-east.omim.org/phenotypicSeriesTitle/all"):
		# Input is the webpage link for all the phenotypicSeries titles (table 
		# of omim ids each as a representative of a PS).
		# For method "series_links", must be the "title" page with one main table 
		# of omim description and the omim id of the representative entry of the omim 
		# series.  It is not the page with a table of ids for each series!!!
		# east coast mirror (default) and main page
		# http://us-east.omim.org/phenotypicSeriesTitle/all
		# http://www.omim.org/phenotypicSeriesTitle/all
		self.ps_page = ps_page

	def series_links(self,ps_page=None):
		# USES SCREENSCRAPE AND NOT API
		# screen scrapes all phenoseries pages to produce list of links to all phenotypicSeries 
		# pages. 
		# For this method, must be the "title" page with one main table 
		# of omim description and the omim id of the representative entry of the omim 
		# series.  It is not the page with a table of ids for each series!!!
		# east coast mirror (default) and main page
		# http://us-east.omim.org/phenotypicSeriesTitle/all
		# http://www.omim.org/phenotypicSeriesTitle/all
		# Input link overrides constructor default self.ps_page.
		# The page's results table has "a" tags for each of the PS rep ids and a link to a page 
		# for that series. Skips rep ids leading to bad link or inconsistent info. Returns a list 
		# of two-tuples having (omim rep id,link to PS page). Each tuple is a phenotypicSeries.
		# returns None is no data found or bad link provided.
		links = list()

		# override default link in constructor
		if ps_page is not None:
			self.ps_page = ps_page

		# get domain 
		location = urlparse(self.ps_page).netloc

		# fetch page finding the table of links
		ps_div = bs4.BeautifulSoup(req.get(self.ps_page).text.replace("\n","")).find("div",id="results")
		
		if ps_div is None: # None if broken link/no ps info
			return None
		else:
			# find_all "a" tags each a series
			for series_tag in ps_div.find_all("a"):
	
				series_page = "http://"+location+series_tag.get("href")
				series_id = str(series_tag.string)
			
				links.append((series_id,series_page))
			
		return links

	def all_info(self,rep_links):
		# get all the information for each entry of all phenotypicSeries'
		# input is a list of links to individual PS pages. list elements are 2-tuples of 
		# (representative phenotype id,series link).  Output is a dict of lists and 
		# is relatively big.  Returns dict with PS rep omim id as key, list of lists as 
		# value.  The list of lists is made in method self.sub_series() and is described there
		all = dict()
		
		# follow each link to individual PS webpages
		for rep in rep_links:
			all[rep[0]] = self.sub_series(rep[1])
		
		return all

	def sub_series(self,link):
		# pull out all member diseases from an individual phenotypicSeries page
		# link is to the webpage of a specific phenotypicSeries
		# link will most likely be of form 'http://www.omim.org/phenotypicSeries/400044'
		#
		# returns list of lists.  Each list is an omim phenotype together making up the 
		# list of entries for a phenotypicSeries
		# for each entry's list there are these 6 element strings:
		# 1. cytogenic location, 2. omim description, 3. mapping key, 4. omim phenotype id, 
		# 5. gene symbol(s), 6. omim gene id
		# Attention!: there may be duplicate rows of series id<tab>member id as 
		# one omim id may have two different descriptions and have two different 
		# rows in the table of each phenotypic series!

		# logic:
		#    1. find the table from div "phenotype-map-table border" in var tbl_class
		#    2. find_all tr, skip without tds having class name in var td_class below
		#    3. iterate through each td with embedded "a" tag" and populate a dict with contents
		#
		# NOTES: each row has many elems, but only the six tds containing an "a" tag are 
		#    desirable. This means there are 6 valuable "a" tag strings translating to 
		#    the 6 ordered list elements. Returns None if given a bad link.

		# class names to find
		tbl_class = "phenotype-map-table border"
		td_class = "phenotype-map-value text-font value-border" # class name for value cells of table

		# list for entire to contain a list for
		entries = list()
		
		# TABLE: get results table
		tbl = bs4.BeautifulSoup(req.get(link).text.replace("\n","")).find("table",class_=tbl_class)
		
		# bad link or listed as representative id to a series, then listed as not having a PS
		if tbl is None:
			return None
		
		# ROWS: pull out the rows of the table with values 
		trs = tbl.find_all("tr")
		
		for tr in trs:
			
			# use only row that has a td of the class name above in var td_class
			tds = tr.find_all("td",class_=td_class)
			
			# find all tds in row if row has 6 tds in it
			if tds is not None and len(tds) == 6:
			
				entry = list()
				## "A" TAGS: add contents of 6 ordered "a" tags 				
				#for a_tag in tr.find_all("a"):
				#	entry.append(str(a_tag.string))

				# go through the 6 tds, if link ("a" tag), find content, otherwise 
				# content of td is a string
				for td in tds:
					
					# look in contents for a_tag, if content of td does not have 
					# a tag ("a" tag) within it, just add the content string of the td
					try:
						a_tag = td.contents[0].find("a")
						entry.append(str(a_tag.string))
					except:
						entry.append(td.contents[0])

				entries.append(entry)
			elif tds is not None and len(tds) > 0:
				print "Wrong: "+str(tds)
				exit(0)
		return entries
		