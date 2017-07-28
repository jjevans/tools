import json
import requests as req
import xml.etree.ElementTree as ET

''' utilize the OMIM api to retrieve data via web service '''
''' api key for 2014 2EF035ECBD2E73BA368BECD371EA3E9E35D84034 '''

class Use():

	def __init__(self,apikey,url="http://api.omim.org/api"):
		self.key = apikey
		self.url = url # url without handler
		
		self.pars = {"apiKey" : self.key,
			"format" : "json"}
			
	def get_req(self,handyurl):
		try:
			response = json.loads(req.get(handyurl,params=self.pars).text)
		except ValueError:
			response = None
			
		return response
		
	def geneMap_by_att(self,response,attribute):
		# returns a list of results by desired geneMap attribute
		
		res = list()
		
		if response is not None:
			for genemap in response["omim"]["listResponse"]["geneMapList"]:
				res.append(genemap["geneMap"][attribute])
			
		return res
		
	def omim_by_location(self,chr,start,end):
		handyurl = self.url + "/geneMap"
		self.pars["chromosome"] = chr
		
		# WHY DOESN'T THIS WORK?
		#self.pars["chromosomeLocationStart"] = start
		#self.pars["chromosomeLocationEnd"] = end

		response = self.get_req(handyurl)

		return self.geneMap_by_att(response,"mimNumber")
	
	def omim_by_chr(self,chr):
		handyurl = self.url + "/geneMap"
		self.pars["chromosome"] = chr
		
		response = self.get_req(handyurl)
		
		return self.geneMap_by_att(response,"mimNumber")
		
	def all_omim(self):
		handyurl = self.url + "/geneMap"
		
		response = self.get_req(handyurl)
		
		return self.geneMap_by_att(response,"mimNumber")
				
	def sym_by_omim(self,omim):
		handyurl = self.url + "/geneMap"
		self.pars["mimNumber"] = omim
		
		response = self.get_req(handyurl)

		return self.geneMap_by_att(response,"geneSymbols")

	def variant_by_omim(self,omim):
		handyurl = self.url + "/entry/allelicVariantList"
		self.pars["mimNumber"] = omim
		
		response = self.get_req(handyurl)
		
		return response

class Pheno():
	# get information for a given phenotype
	
	def __init__(self,apikey,url="http://api.omim.org/api"):
		self.key = apikey
		self.pars = {"apiKey" : self.key}
		
		self.url = url

	def get_req(self,handyurl):
		return json.loads(req.get(handyurl,params=self.pars).text)	
		
	def get_genes(self,omim):
		# takes an omim phenotype number and gets the genes associated with it
		handyurl = self.url + "/entry"
		self.pars["mimNumber"] = omim
		self.pars["include"] = "geneMap"
		
		xml = req.get(handyurl,params=self.pars).text
		
		res = dict() # use keys to sort unique

		try: # xml provided back (errors provide html)			
			elem = ET.fromstring(xml)

			for symbols in elem.iter(tag="geneSymbols"):
				for sym in symbols.text.split(", "):
					res[sym] = None
		
			if len(res.keys()) == 0:
				return None

		except: # html error returned
			return "Error"

		return res.keys()
		
	def pheno_series(self,omim):
		# takes a omim number and queries for the phenotypicSeries 
		handyurl = self.url + "/entry"
		self.pars["mimNumber"] = omim
		self.pars["include"] = "all"
		
		xml = req.get(handyurl,params=self.pars).text
		
		elem = ET.fromstring(xml)
		
		for series in elem.iter(tag="phenotypicSeriesMimNumber"):
			print series.text
			
			
		return
			
class Search():

	def __init__(self,apikey,url="http://api.omim.org/api"):
		self.key = apikey
		self.url = url # url without handler
		
		self.pars = {"apiKey" : self.key}
			
	def omim_by_search(self,terms):
		# input is a string of space separated search terms
		
		handyurl = self.url + "/entry/search"
		self.pars["search"] = terms
		
		response = req.get(handyurl,params=self.pars).text
		
		res = self.omim_from_xml(response)
		
		return res

	def omim_from_xml(self,xml):
		# get the omim ids from a returned xml (search)

		try:
			elem = ET.fromstring(xml)
		
			res = list()
			for omim in elem.iter(tag="mimNumber"):
				res.append(omim.text)
		except:
			print "\nerror at omim_from_xml, not valid xml.\n"
			print xml+"\n"
			return list()

		return res