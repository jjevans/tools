import rpy2.robjects as rob


class Util():
	####
	# initiate biomaRt obj
	####
	
	def __init__(self,mart=None,set=None):

		self.mart = mart
		self.set = set
		
		rob.r.library('biomaRt')
		
		# declare to biomaRt which mart to use
		if mart is not None:
			self.mart_obj = self.useMart(self.mart)
			
			if set is not None:
				# declare dataset type if provided
				self.mart_obj = self.declareSet(self.mart_obj,set)
		else:
			self.mart_obj = None
			
	def useMart(self,mart):
		# produces simple mart, no dataset declared, must declare before use
		if mart is None:
			raise ValueError("mart can't be None")
			
		return rob.r.useMart(mart)
		
	def declareSet(self,mart=None,set=None):
		if mart is None:
			raise ValueError("mart can't be None")
		elif set is None:
			raise ValueError("dataset can't be None")
			
		return rob.r.useDataset(set,mart=mart)
		
	def listMarts(self):
		return rob.r.listMarts()
	
	def listSets(self):
		if self.mart_obj is None:
			raise ValueError("mart can't be None")
			
		return rob.r.listDatasets(self.mart_obj)
	
	def listFilters(self):
		if self.mart_obj is None:
			raise ValueError("mart can't be None")
		elif self.set is None:
			raise ValueError("dataset can't be None")
		
		return rob.r.listFilters(self.mart_obj)
	
	# using the mart object, query biomart with inputted 
	#	attributes in this class object
	def ask(self,atts,filts,vals):
		# atts, filts, vals are lists
		ans = rob.r.getBM(attributes=atts, filters=filts, values=vals, mart=self.mart_obj)
		
		return ans
	
class Query():
	####
	# Formulate queries.
	# Canned queries for diff types of ids
	####
	
	# ids are always a list object
	
	def __init__(self,mart=None,set=None):
		self.mart_obj = Util(mart,set)
			
	def ask(self,atts,filts,vals):
		# overloads ask function in class Util()
		# atts is the input value types, filts is the output value type,
		#  vals is the values to be used (ids, etc.)
		# atts (attributes) filts (filters) and vals (values) are lists
		ans = self.mart_obj.ask(atts,filts,vals)
		
		return ans
		
	# canned query to take hgnc id and convert it 
	#	to ensembl id
	def hgnc_to_ensembl(self,ids):
		att_from = "hgnc_symbol"
		att_to = ["ensembl_gene_id","hgnc_symbol"]
		
		return self.ask(att_to,att_from,ids)
		
	# canned query to take ensembl id and convert it 
	#	to the hgnc symbol
	def ensembl_to_hgnc(self,ids):
		att_from = "ensembl_gene_id"
		att_to = "hgnc_symbol"
		
		return self.ask(att_to,att_from,ids)
	
	# convert from hgnc to entrez gene id
	def hgnc_to_entrez(self,ids):
		att_from = "hgnc_symbol"
		att_to = "entrezgene"
		
		return self.ask(att_to,att_from,ids)

	# convert from entrez to hgnc
	def entrez_to_hgnc(self,ids):
		att_from = "entrezgene"
		att_to = hgnc_symbol
		
		return self.ask(att_to,att_from,ids)
		
	'''		
	# get go from a gene name hugo
	# UNFINISHED!!!
	def hgnc_to_go(self,ids):
		att_from = "hgnc_symbol"
		att_to = "goslim_goa_description"
		
		
		for x in xrange(0,len(ids)):
			self.query = ids[x]
			self.getit()
			converted.append(self.answer)
			print identifiers[x]
			print self.answer
			
		self.to_convert = identifiers
		self.converted = converted
		
		return self.converted
		
	def entrez_to_goid(self,identifiers):
		self.db = "ensembl"
		self.set = "hsapiens_gene_ensembl"
		self.att_from = "entrezgene"
		self.att_to = "go_id"

		converted = list()

		for x in xrange(0,len(identifiers)):
			self.query= identifiers[x]
			self.getit()
			converted.append(self.answer)
			
			#rob(self.answer(1))

			print self.query
			print self.answer.rx2(1)

#			for y in xrange(0,len(self.answer)):
#				print y+"\t"+self.answer[y]
			#print identifiers[x]
			#print self.query+"\t"+str(self.answer)

		self.to_convert - identifiers
		self.converted = converted

		return self.converted

	def entrez_to_goinfo(self,identifiers):
		db = "ensembl"
		set = "hsapiens_gene_ensembl"
		att_from = "entrezgene"
		att_to = "go_id"

		go_name = "name_1006"
		go_def = "definition_1006"
		go_evid = "go_linkage"
		go_domain = "namespace_1006"

                atts = ["entrezgene","go_id","name_1006","definition_1006","go_linkage_type","namespace_1003"]

		rob.r.library('biomaRt')

		smart = rob.r.useMart(db, dataset = set)

		for x in xrange(0,len(identifiers)):

			GO_Info = rob.r.getBM(attributes=atts,filters="entrezgene", values=identifiers[x], mart=smart)
			
			for y in xrange(0,len(GO_Info[0])):
				print str(GO_Info[0][y])+"\t"+str(GO_Info[1][y])+"\t"+str(GO_Info[2][y])+"\t"+str(GO_Info[3][y])+"\t"+str(GO_Info[4][y])+"\t"+str(GO_Info[5][y])
		
		return
	'''