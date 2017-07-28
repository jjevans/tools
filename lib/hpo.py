import tbl_util

# python module to parse hpo files (human-phenotype-ontology.org)

class Organize():
	
	def __init__(self,file):
		self.file = file
		self.tbl_obj = tbl_util.Table(file)

	def org_by_pheno(self):
		# filename: phenotype_to_genes.txt
		col = 0
		return self.tbl_obj.col_all_cols(col)

	def org_by_entrez(self):
		# filename: phenotype_to_genes.txt
		col = 2
		return self.tbl_obj.col_all_cols(col)

	def org_by_sym(self):
		# filename: phenotype_to_genes.txt
		col = 3
		return self.tbl_obj.col_all_cols(col)
	
	def org_by_hpo(self):
		# filename: phenotype_annotation.tab
		hpo_col = 4
		
		return self.tbl_obj.col_all_cols(hpo_col)

class Combine():
	
	def __init__(self,ptog_dict,pa_dict):
		# file phenotype_to_genes.txt parsed into dict by org_by_pheno
		# file phenotype_annotation.tab parsed into dict by org_by_col1
		#
		
		self.phenotype_to_genes = ptog_dict
		self.phenotype_annotation = pa_dict
	
	def combo(self):
		pass
		
