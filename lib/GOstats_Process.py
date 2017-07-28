import math
import rpy2.robjects as rob
from rpy2.robjects.packages import importr

''' parse and merge multiple GOstats results, create pheatmap heatmap '''

class Merge():
	''' take multiple gostat summary lists and produce a dict of lists of 
		the values (pval or other) '''
		
	def __init__(self):
		# do I need this?
		pass
	
	def term_by_val(self,smry,hot_col=1):
		''' get the values out of a GOstats 
			summary list of lists and organize by term. returns a dict of 
			for each GO id.  GO id is concated to the GO description in the 
			key and the column to be in heatmap as the value.  
			input is GOstats summary and a column of the value to be put in 
			heatmap 
			
			GOstats Columns
			GO ID - smry[0]
			pval - smry[1]
			oddratios - smry[2]
			expected - smry[3]
			observed - smry[4]
			gene count - smry[5]
			GO description - smry[6] '''
		
		desc_len = 80 # num chars to limit description to
		delim = "::" # delimiter to concat GO id with its description
		id_col = 0
		desc_col = 6
		
		# each GO Id, key of ID concat to term description and value to be 
		# in heatmap as value, trim description to desc_len chars
		terms = dict()
		for i,term in enumerate(smry[id_col]):
			desc = str(smry[desc_col][i])[:desc_len]
			term += delim+desc
			value = smry[int(hot_col)][i]
			
			# desired column, if None or empty list returns a None in value
			# if column in cols is a string, take the -log2 value
			# strings get -log2
			if isinstance(hot_col,str) and value is not 0:
				value = self.neg_log2(value)
					
			terms[term] = value

		return terms
		
	def term_merge(self,term_dicts,null_val=0):
		# create a 3-D array.
		# each GO Id as key in term_dicts has an array of gene sets 
		# associated.  Each gene set has an array of values.  takes a dict 
		# with GO Id as key with an array of arrays as value.
		# a list of values that are pushed onto the gene set list.  starts up 
		# with an array of dictionaries
		mat = dict()
		
		for i,set in enumerate(term_dicts):			
			for term in set.keys():

				if term not in mat.keys():
					# no current record, create a new empty record
					mat[term] = list([null_val]*len(term_dicts))
		
				mat[term][i] = set[term]
			
		return mat

	def build_mat(self,structure,colnames=None):
		''' create a matrix and convert to rpy data.frame '''
		# input is a dict with GO term as id and a list as values.
		# Each gene set has a list for each GO term.  The names of each gene 
		# set is inputted in the list 'colnames'. 
		# keep track of the order of keys		
		# make linear (single sequence) to load into R data frame.
		# creates a r matrix with row as term and col as gene sets
		
		linear = list()
		rownames = list()
		for term in structure.keys():	
			linear.extend(structure[term])
			rownames.append(term)
			
		# make column names empty strings if no names provided
		if colnames is None:
			colnames = list([""] * len(structure[term][0]))
		
		# populate R matrix
		r_mat = rob.r.matrix(data=rob.FloatVector(linear), nrow=len(rownames), ncol=len(colnames), dimnames=[rob.StrVector(rownames), rob.StrVector(colnames)], byrow=True)
		
		return r_mat
		
	def neg_log2(self,value):
		try:
			value = math.log(value,2)*-1
		except ValueError:
			print "value must be loggable at log2"

		return value

	def min_overlap(self,mat,num_overlap,null_val=0):
		# remove the terms in python dict that have less than num_overlap 
		# gene sets with an entry for that term, return a new dict or None 
		# if no terms meet the criteria.
		
		keeper = dict()
		for term in mat.keys():
			
			count = 0
			for val in mat[term]:
				
				if val is not null_val:
					count += 1
			
			# needs to be coerced to ints for some reason, need to fix.
			if int(count) >= int(num_overlap):
				keeper[term] = mat[term]
				
		return keeper
			
class Heatmap():
	''' create a heatmap in R from an R data.frame/matrix '''
	def __init__(self,r_mat=None,file=None):
		# option to provide matrix and output filename when initializing.
		# otherwise acceptable to wait for the actual call to produce 
		#  heatmap to do so
		self.mat = r_mat
		self.file = file
	
	def pretty_hm(self,r_mat=None,file=None):
		# use R pheatmap
		# create heatmap file
				
		if r_mat is None and self.mat is None:
			raise Exception("A matrix needs to be provided at pretty_hm()")
		if file is None and self.file is None:
			raise Exception("A filename needs to be provided at pretty_hm()")
		
		phm = importr("pheatmap")
		rcb = importr("RColorBrewer")
		
		w = 10.5
		h = self.find_h(r_mat)
		cw = 10 #cell width
		ch = 10 #cell height
		fs = 1
		
		# rcolorbrewer, include white for null (0) values
		ncolor = 5
		spectrum = "YlOrRd"
		palette = "brewer.pal("+str(ncolor)+",'"+spectrum+"')"		

		rob.r.pheatmap(r_mat, filename=file, cellwidth=cw, cellheight=ch, color=rob.r.c("#FFFFFF",rob.r(palette)), width=w, height=h, font_size=fs, cluster_cols=False)
				
		return file

	def find_h(self,r_mat,per_row=0.15):
		''' based on the number of rows in the matrix determine the height 
			of the output pdf/png, per_row is the number of inches per row 
			of results in r_mat '''

		# number of inches for the top and bottom margin + all the rows
		marg = 4
		num_row = rob.r.length(rob.r.rownames(r_mat))[0]
		
		return num_row * per_row + marg

