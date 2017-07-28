# breaks tab delimited strings into various data structures

class TableList():
	# break table output into lists of lists
	# The basic list is of rows with each 
	# row being a list of columns
	
	def __init__(self):
		pass
		
	def dump(self,tabdelim):
		# return a list of lists 
		# of values from a tab 
		# delimited string
		# header unaccounted for
		table = list()
		
		lines = tabdelim.split("\n")
		for line in lines			
			table.append(line.split("\t"))
	
		return table


# TRY BELOW OUT, UNTESTED !!!	
'''
class Table():
	
	def __init__(self,file):
		self.file = file
		
	def col_by_col(self,col1,col2):
		''' take a text table file and organize a dictionary with the col1 
			as key and a list of contents in col2 as value '''
			
		content = dict()
		with open(self.file) as handle:
			for line in handle:
				if line.startswith("#"):
					continue
				
				cols = line.rstrip().split("\t")

				primary = cols[col1]
				
				if not primary in content:
					content[primary] = list()
					
				content[primary].append(cols[col2])
				
		return content
	
	def col_all_cols(self,col):
		''' take a text table file and create a dictionary of a list of lists '''
		# inputted col number to use as key and the columns in a list split by tab 
		# put in a list (list of lists)
		
		content = dict()
		with open(self.file) as handle:
			for line in handle:
				if line.startswith("#"):
					continue
					
				cols = line.rstrip().split("\t")
				
				primary = cols[col]

				if not primary in content:
					content[primary] = list()
					
				content[primary].append(cols)
				
		return content
'''
