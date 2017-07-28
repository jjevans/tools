import rpy2.robjects as rob

######
######
######
######	
	
class Use():
	'''	
	Class to run the GOstats tests.  Meant to be the interface to those 
	using this module
	'''

	def __init__(self,ids,ont="BP",db="org.Hs.eg",pcut=0.05):
		# ids are in a list
		
		cond = True
		direct = "over"
	
		# Remove all empty values in the list of ids.
		num_empty = ids.count("")
		for i in range(num_empty):
			ids.remove("")			
		
		self.interface_obj = Interface_R(ids,ont,db,cond,pcut,direct)
		
	def run(self):
		'''run one ontology, calls GOstats_R.Interface_R.single_run() which does the work'''
		return self.interface_obj.single_run()
				
	def get_param(self):
		""" store the parameters used in the run under param string """
		return self.interface_obj.get_param()

				
######
######
######


class Interface_R():
	''' Class to run GOstats in R, call GOstats library, call library of 
		genome annotations defaults to 'org.Hs.eg.db' '''

	def __init__(self,ids, ont="BP", base_db="org.Hs.eg", cond=True, pcut=0.01, direct= "over", univ=None,par_name="gostats_par"):
		''' set the result obj to None.  This will be replaced once the 
			HyperGResult obj is created with HyperGTest, res_obj is None 
			and represents an instance of class Res (below) created from the 
			self.res HyperGResult obj.  Both of these are populated in 
			run_test() '''
		
		self.res = None
		self.res_obj = None
		
		# name in R of the soon to be built HyperGParam obj, used 
		#  later to create an instance of that named par obj in 
		#		R environment
		self.par_name = "gostats_par"
	
		# set parameters 
		self.ids = ids
		self.base_db = base_db
		self.db = base_db+".db"
		self.ont = ont
		self.cond = cond
		self.pcut = pcut
		self.direct = direct

		# call libraries 'GOstats' and database for Entrez accession. 
		#	Silences output to terminal while it does so.
		rob.r.library("GOstats")
		rob.r.library(self.db) 
		
		# pull out all Entrez ids for the reference universe genes 
		if not univ:
			univ = self.create_univ()
 
		# set universe parameter
		self.univ = univ

	def create_univ(self):
		''' produce the reference set of genes, the gene universe '''
		
		accnum_db = self.base_db+"ACCNUM"
		acc_str = rob.r[accnum_db]
		
		return rob.r['mappedkeys'](acc_str)

	'''
	###
	# Make HyperGParams object, run hyperGTest, self.res = HyperGResult obj
	### 
	'''
	
	def single_run(self):
		''' complete GOstats test by producing the parameter object and
	  running the test, results go in self.res '''
		
		# make the HyperGParam obj
		self.make_par()
		
		# run the GOstat test and use a hyperGResult object to produce an 
		# object of class res below
		hg_res = self.run_test()
		
		return Res(hg_res)
	
	def run_test(self):
		''' take the R globalEnv located HyperGParam obj and run 
	  		HyperGTest, returns the HyperGResult obj '''
		
		return rob.default_ri2py(rob.r.hyperGTest(rob.r[self.par_name]))
		
	def make_par(self):
		''' create GOstats parameter object, produce a data frame in R of the 
			ids of the test gene list and another of the gene universe, create 
			R vars for all params in the global environment '''
			
	 	rob.globalenv['geneIds'] = rob.StrVector(self.ids)
		rob.globalenv['univIds'] = rob.StrVector(self.univ)
		rob.globalenv['anno'] = self.db
		rob.globalenv['ont'] = self.ont
		rob.globalenv['pcut'] = self.pcut
		rob.globalenv['cond'] = self.cond
		rob.globalenv['direct'] = self.direct
		
		# produce the R GOstats parameter object using the var par_name
		rob.globalenv[self.par_name] = rob.r('''new("GOHyperGParams", geneIds=geneIds, universeGeneIds=univIds, annotation=anno, ontology=ont, pvalueCutoff=as.numeric(pcut), conditional=as.logical(cond), testDirection=direct)''')
		
		return

	def get_param(self):
		''' returns the parameters in the form of ontology, annotation, p-value
			cutoff, if conditional test or not, an over or under-
	 		represented test '''
		
		out_str = "ontology = "+self.ont+"   \n"
		out_str += "annotation = "+self.db+"   \n"
		out_str += "pvalue_cutoff = "+str(self.pcut)+"   \n"
		out_str += "conditional = "+str(self.cond)+"   \n"
		out_str += "direction = "+self.direct+"   \n"
	
		return out_str

	'''
	###
	#	Several methods to change a parameter in the self object.  
	###
	'''
	
	def set_par_name(self,name):
		''' change the name of the HyperGParam object in the R globalEnv '''
		
		rob.globalenv[self.par_name] = name
		self.par_name = name
		
		return
		
######
######
######
######
class Res():
	'''	Class to fetch the information from a GOstats HyperGResult obj. '''
	
	def __init__(self,hg_res_obj):
		''' takes as argument a HyperGResult object'''
		
		self.hg_res_obj = hg_res_obj
		
		rem_vec = self._find_removed()
		self.rem = self._vec_to_str(rem_vec)
		
	'''
	Below are the methods to fetch the results from the GOstats 
	HyperGResult object
	'''
	
	def removed(self):
		''' returns the gene ids in the set of interesting genes (test set) 
		that did not exist in the gene universe (reference set).  Uses 
		method _find_removed to retrieve the ids and returns the list '''
		return self.rem
			
	def _find_removed(self):
		''' retrieves the ids in the test set that don't exist in the 
	  	gene universe set, requires objects 'geneIds' and 'univIds' 
	  	exist in the R environment most likely produced in method make_par '''
		return rob.r('''geneIds[!geneIds %in% univIds]''')

	def _vec_to_str(self,StrVector):
		''' convert an R StrVector to a string, takes a StrVector as 
		input and returns a string with each element from the vector 
		separated by a single whitespace (" ") '''
		
		converted = str()
		for elem in StrVector:
			converted += elem+" "

		# pull off the trailing space
		converted.rstrip()
		
		return converted
		
	def summary(self):
		''' get the summary table from the gostats result object '''
		return rob.r.summary(self.hg_res_obj)
		
	def smry_dict(self):
		''' parse the summary and create python dictionary containing
		each term as key '''
		
		smry_tbl = self.summary()
		
		''' go through each GO term and concatenate desired results into str.
			Format: GO_term<tab>pval<tab>expected<tab>observed<tab>gene_count<tab>description
			
			GO ID - smry_tbl[0]
			pval - smry_tbl[1]
			#oddratios - smry_tbl[2]
			expected - smry_tbl[3]
			observed - smry_tbl[4]
			gene count - smry_tbl[5]
			GO description - smry_tbl[6] '''
	
		go_dict = dict()
		for i,x in enumerate(smry_tbl[0]):
			go_str = str()
			go_str += smry_tbl[0][i]+"\t"
			go_str += str(smry_tbl[1][i])+"\t"
			#go_str += str(smry_tbl[2][i])+"\t"
			go_str += str(smry_tbl[3][i])+"\t"
			go_str += str(smry_tbl[4][i])+"\t"
			go_str += str(smry_tbl[5][i])+"\t"
			go_str += str(smry_tbl[6][i])+"\n"

			# organize in dictionary a string of stats as value, GO Id as key
			go_dict[smry_tbl[0][i]] = go_str
			
		return go_dict
			
	def annotation(self):
		''' get the annotation (db) used for the test '''
		return rob.r.annotation(self.hg_res_obj)[0]
		
	def description(self):
		''' retrieve the user input parameter 'description' '''
		return rob.r.description(self.hg_res_obj)[0]

	def conditional(self):
		'''determine whether the test used a conditional hypergeometric test '''
		return rob.r.conditional(self.hg_res_obj)[0]

	def testname(self):
		''' retrieved the type of ontology (usually GO unless you 
	  change ie. KEGG) and which ontology (BP,MF,CC) branch '''

		testName = rob.r.testName(self.hg_res_obj)
		
		type = testName[0]
		branch = testName[1]

		return type+" "+branch
		
	def mappedcount(self):
		''' get the number of gene universe mapped in all '''
		return rob.r.geneMappedCount(self.hg_res_obj)[0]

	def geneIdsByCategory(self):
		''' gets the gene ids for each GO term '''
		return rob.r.geneIdsByCategory(self.hg_res_obj)
	
	def pvalues(self):
		''' get the p-values for each GO term '''
		
		pvals = rob.r.pvalues(self.hg_res_obj)
		
		pval_dict = {}
		for i, x in enumerate(pvals):
			pval_dict[pvals.names[i]] = x
		
		return pval_dict
		
	def oddratios(self):
		''' get the odds ratio for each GO term '''
	
		oddrats = rob.r.oddRatios(self.hg_res_obj)
		
		or_dict = {}
		for i, x in enumerate(oddrats):
			or_dict[oddrats.names[i]] = x
			
		return or_dict
	
	def expected(self):
		''' get the expected counts for each GO term '''
	
		expect = rob.r.expectedCounts(self.hg_res_obj)
		
		expect_dict = {}
		for i, x in enumerate(expect):
			expect_dict[expect.names[i]] = x
			
		return expect_dict
		
	def observed(self):
		''' get the observed counts for each GO term '''
		
		observe = rob.r.geneCounts(self.hg_res_obj)
		
		observe_dict = {}
		for i, x in enumerate(observe):
			observe_dict[observe.names[i]] = x
			
		return observe_dict
