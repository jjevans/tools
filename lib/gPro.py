import re
import requests as req

##
# Class to run g:Profiler queries
# g:GOst (class Profiler), g:Convert (class Convert_ID)
#
#
####
# Jason Evans, 10152011
####

class To_and_fro():
	''' perform the queries through http, requires the url  '''
	def __init__(self,loc):		
		self.loc = loc
		
	def ask(self,info):
		''' query gPro tool url for parameters '''
		req_obj = req.post(self.loc,info)
		
		return req_obj.content
		
class Profiler():
	''' use GOst tool, Note: look in actual gProfiler url for params '''
	def __init__(self,loc,spec='hsapiens',prefix='ENTREZGENE_ACC'):
		
		# keep all comment information and the results
		self.info = list()
		self.res = list()
		
		#params
		out = "mini" #text
		#out = "txt" #html
		sort = 1
		signif = 0
		def_pcut = 0.25 #default p-value cutoff, reassigned in ask_pcut()
		
		self.pars = {"organism":spec,"query":"","output":out,"prefix":prefix, "sort_by_structure":sort, "significant":signif, "term":"", "user_thr":def_pcut}

		self.tnf_obj = To_and_fro(loc)
		
	def ask(self,ids):
		self.pars["query"] = ids
		
		return self.tnf_obj.ask(self.pars)

	def ask_pcut(self,ids,pcut):
		if float(pcut) > 1 or float(pcut) <= 0:
			raise Exception("P-value cutoff must be 0 < pcut <= 1.")
		
		self.pars["query"] = ids
		self.pars["user_thr"] = pcut
		
		return self.tnf_obj.ask(self.pars)

	def GO_ask(self,term):
		''' enrich with the gene set for GO term accession '''
		self.pars["term"] = term
		
		return self.tnf_obj.ask(self.pars)

	def break_GOSt(self,content,col_num=(9,8,2,5,11,12)):
	
		# col_num is a tuple of which columns to report
		# columns to bring out of the returned table
		# cols 9=source, 8=term id, 2=p-value, 5=number of genes enriched, 
		# 11=term description, 12=hierarchy level
		#col_num = 0,1,2,3,4,5,6,7,8,9,10,11,12
			
		self._organize_GOSt(content,col_num)
		
		return "\n".join(self.res)+"\n"
	
	def _organize_GOSt(self,content,col_num):
		''' parse GOst output from text table output (not html)'''
		
		for line in content.split("\n"):
			if "No results found" in line:
				self.res.append("No results found.")
				break
			if line == "":
				continue
			elif line.startswith("#"):
				self.info.append(line)
			else:
				data = self._fetch_col(line,col_num)
				nl = self._prep_line(data)
				self.res.append(nl)
	
		return
		
	def _fetch_col(self,line,col_num):
		''' takes tab delimited line and a int or tuple of columns to fetch '''
		
		cols = line.split("\t")
		
		data = list()
		
		# if multiple columns desired (list) single column desired (int)
		if isinstance(col_num,int):
			data.append(cols[col_num])
		else:
			for i in col_num:
				data.append(cols[i])

		return data
	
	def justGO(self,content):
		# return only the lines that have GO terms
		# column 8 has the ontology type to check
		col_num = 8
		
		self._organize_GOSt(content,col_num)
		
		only_GO = str()
		for id in self.res:
			if self._id_isGO(id):
				only_GO += id+"\n"
				
		return only_GO

	def _GOSt_type(self,line):
		# get ontology type from line
		cols = line.split("\t")
		return cols[9]
		
	def _id_isGO(self,id):
		match = "GO:"
		
		if match in id:
			return True
			
		return False
		
	def _isGO(self,label):
		# see if inputted label is any of the ontology types
		types = "BP","CC","MF"
		
		if label in types:
			return True
		
		return False

	def _prep_line(self,data):
		# fix so no leading tab
		nl = str()
		for col in data:
			nl += col+"\t"
				
		return nl.rstrip("\t")
	
class Convert_ID():
	''' organism=hsapiens&target=HGNC&output=html&query=MT:1:16569&region_query=on&prefix=AFFY_HUGENE_1_0_ST_V1 '''
	def __init__(self,loc="http://biit.cs.ut.ee/gprofiler/gconvert.cgi", spec="hsapiens", prefix="ENTREZGENE_ACC"):
		''' use g:Convert tool, hint: look in url for params '''
		# always specifies a numeric id as an Entrez Gene id
		
		#params
		out = "mini" #text
		#out = "txt" #html
		
		self.pars = {"organism":spec,"query":None,"prefix":prefix, "target":None, "output":out}

		self.tnf_obj = To_and_fro(loc)
		
	def ask(self,ids,target):
		self.pars["query"] = ids
		self.pars["target"] = target
			
		return self.tnf_obj.ask(self.pars)
		
	# canned queries for id conversion
	def to_entrez(self,ids):
		target = "ENTREZGENE_ACC"
		
		ans = self.ask(ids,target)
		col = self._uniq_col(ans)
		
		return "\n".join(col).replace("ENTREZGENE_ACC:","")
				
	def to_ensg(self,ids):
		target = "ENSG"
		
		ans = self.ask(ids,target)
		col = self._uniq_col(ans)
		
		return "\n".join(col)+"\n"
				
	def to_hgnc(self,ids):
		target = "HGNC"
		
		ans = self.ask(ids,target)
		col = self._uniq_col(ans)
		
		return "\n".join(col)+"\n"
		
	def _uniq_col(self,content): #removes N/A
		# grab the id from col 3 in gPro results, skip
		# any "N/A" (no match) and remove duplicates
		col_num = 3
		
		data = list()
		for line in content.rstrip().split("\n"):
			cols = line.split("\t")
			
			if "N/A" not in cols[col_num]:
				data.append(cols[col_num])	
		
		uniq = self._unique(data)
		
		return tuple(uniq)
		
	def _unique(self,lst):

		set = {}
		map(set.__setitem__, lst, [])
		
		return set.keys()


''' sample url
		
#http://biit.cs.ut.ee/gprofiler/index.cgi?organism=scerevisiae&query=swi4+swi6+mbp1+mcm1+fkh1+fkh2+ndd1+swi5+ace2&r_chr=X&r_start=start&r_end=end&analytical=1&domain_size_type=annotated&term=&significant=1&sort_by_structure=1&user_thr=1.00&output=png&prefix=ENTREZGENE_ACC
'''
