import requests as req
import xml.etree.ElementTree as ET

# module to use NCBI etuils

class Eutils():

	def __init__(self,url):
		self.url = url

	def summary_by_entrez(self,entrezids):
		# entrezids is a list of entrez accessions

		strids = list(map(str,entrezids))
		
		ids = ",".join(strids)
		
		self.params = {"db":"gene","id":ids,"retmode":"xml"}
		
		xml = req.get(self.url,params=self.params).content
		print xml
	
		"""	
		elem = ET.fromstring(xml)
		
		res = dict()
		for desc in elem.iter(tag="Gene-ref_desc"):
			res[str(entrezids.pop(0))] = desc.text
			
		return res
		"""
		
		return

	def desc_by_entrez(self,entrezids):
		# entrezids is a list of entrez accessions
		
		strids = list(map(str,entrezids))
		
		ids = ",".join(strids)
		
		self.params = {"db":"gene","id":ids,"retmode":"xml"}
		
		xml = req.get(self.url,params=self.params).content

		elem = ET.fromstring(xml)
		
		res = dict()
		for desc in elem.iter(tag="Gene-ref_desc"):
			res[str(entrezids.pop(0))] = desc.text
			
		return res

		