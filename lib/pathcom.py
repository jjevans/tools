import re
import requests as req
from xml.etree.ElementTree import XMLParser

class To_and_fro():
	''' perform the queries through http, requires the url  '''
	
	def __init__(self,loc):
		self.loc = loc

	def ask(self,info):
		''' query url for inputted parameters '''
		req_obj = req.post(self.loc,info)

		return req_obj.content

class Pathways():
	''' pathway related queries '''

	# location default is hard-coded
	def __init__(self,loc,spec="9606"):

		self.pars = {
			"version":"3.0",
			"cmd":None,
			"organism":spec,
		}

		self.tnf_obj = To_and_fro(loc)

	def path_by_id(self,ids,type="GENE_SYMBOL"):
		# not sure if need to have an input type type=""
		''' ids are a comma separated list of ids, type is the id type 
			valid types:     UNIPROT,CPATH_ID (pathway commons), ENTREZGENE or 
			GENE_SYMBOL.  Max 25 ids allowed by Pathway Commons'''
			
		self.pars["cmd"] = "get_pathways"
		self.pars["input_id_type"] = type
		
		# no more than twenty-five ids at a time, submit 25 per and concat res
		entities = ids.split(",")
		batch = list()
		content = str()
		for i,entity in enumerate(entities):
			batch.append(entity)
			
			if i != 0 and i % 25 == 0 or i == len(entities)-1:
				batch_str = ",".join(batch)
				self.pars["q"] = batch_str
				
				batch_cont = self.tnf_obj.ask(self.pars)
				
				# pull off header from results
				lines = batch_cont.splitlines()
				head = lines.pop(0)
				content += "\n".join(lines)
				
				batch = list()
				
		return content
		
	def path_entities(self,cpaths,out_id_type="GENE_SYMBOL"):
		
		return self.path_details(cpaths,"gsea",out_id_type)

	def path_details(self,cpaths,output="gsea",out_id_type="GENE_SYMBOL"):
		''' input is a comma separated string of Pathway Commons cpath ids '''
		
		# remove any lines consisting of only ".", from lines NO_PATHWAY_DATA
		ids = cpaths.split(",")
		num_dot = ids.count(".")
		for i in xrange(num_dot):
			ids.remove(".")
		
		cpaths_form = ",".join(ids)
		
		self.pars["cmd"] = "get_record_by_cpath_id"
		self.pars["q"] = cpaths_form
		self.pars["output"] = output
		self.pars["output_id_type"] = out_id_type
		
		return self.tnf_obj.ask(self.pars)
	
class Genes():

	def __init__(self,loc,spec="9606"):
		self.pc_obj = Pathways(loc,spec)
		
	def common_path(self,ids,type="GENE_SYMBOL"):
		''' input is a string of comma-separated gene ids in hgnc '''
		
		# get pathways for genes
		path = self.pc_obj.path_by_id(ids)
		genesets = self.gene_by_path(path)
		
		# find what genes share pathways
		return self.gene_cohort(ids,genesets)

	def gene_cohort(self,ids,genesets):
		''' finds genes from a list of ids that exist in a broad gsea gmt 
			gene set for pathways '''
		
		# find genes that exist in each pathway and load into dict
		common = dict()
		for id in ids.split(","):
			for set in genesets.splitlines():
				print set
				if set == "":
					continue
					
				(desc,source,genes) = set.split("\t",2)
				members = genes.split("\t")
								
				if id in members:
					
					# initialize a list for that pathway where the 1st element 
					# is the pathway source and the key is pathway description
					if not desc in common:
						common[desc] = list()
						common[desc].append(source)
						
					common[desc].append(id)
		
		return common
		
	def gene_by_path(self,path):
		''' input is a string result from PC get_pathways implemented 
			in path_by_id() '''
		
		# parse pathway input for gene id, pathway description, pathway id
		# make dict to contain list of gene ids for each pathway id and another 
		# to keep a description for each pathway id
		cpaths = dict()
		desc = dict()
		
		for line in path.splitlines():
			
			# skip lines with header or if gene not found or no pathway data
			if line == "" or line.endswith("PHYSICAL_ENTITY_ID_NOT_FOUND") or line.startswith("Database:") or line.endswith("NO_PATHWAY_DATA"):
				continue

			cols = line.split("\t")
			gene_id = cols[0]
			path_desc = cols[1]
			path_id = cols[-1]
			
			desc[path_id] = path_desc
			
			if not path_id in cpaths:
				cpaths[path_id] = list()

			cpaths[path_id].append(gene_id) 
			
		# query for genes in pathways
		cpath_str = ",".join(cpaths.keys())

		return self.pc_obj.path_entities(cpath_str,"GENE_SYMBOL")	
		
####
# Unimplemented
####
	#### UNIMPLEMENTED XML PARSE	
	def _unimplement_path_by_id(self,id,spec="9606"):
		
		self.pars["cmd"] = "search"
		self.pars["q"] = id
		
		content = self.tnf_obj.ask(self.pars)

		parser = XMLParser()
		parser.feed(content)
		elem = parser.close()
		
#		print content
		
		print elem.tag
		print elem.attrib

		for path in elem:
			
			print "hear "+path.tag+" "+path.attrib.keys()
		
		return
