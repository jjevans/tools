####
# system call to IntervalStats, Princeton
####
# JJE, 04212012
# Oliver Hofmann
# Bioinformatics Core
# Harvard School of Public Health
####

import subprocess
import sys

class Run():

	def __init__(self,qry,ref,dom):
		self.qry = qry
		self.ref = ref
		self.dom = dom
		
	def execute(self,outfile):
		
		cmd = "IntervalStats -q "+self.qry+" -r "+self.ref+" -d "+self.dom+" -o "+outfile
		
		return subprocess.check_call(cmd,shell=True,stderr=subprocess.PIPE)

	def execute2(self,outfile1,outfile2):
		''' runs both the query and then the reference as query through 
			intervalstats.  Runs intervalstats twice in order to compare '''
		
		# run query as query
		self.execute(outfile1)
		
		# run reference as query
		oldquery = self.qry
		self.qry = self.ref
		self.ref = oldquery
		self.execute(outfile2)
		
		return
		
class Filter():

	def __init__(self):
		pass
	
	def filter_by_pvalue(self,peaks,pcut=0.05):
		''' peaks is a list of lines from IntervalStats each line being a 
			single set of peaks '''
		
		signif = list()
		for peak in peaks:
			if self.is_signif(peak,pcut):
				signif.append(peak)
								
		return signif
		
	def is_signif(self,peak,pcut):
		''' input is a line from interval stats results. last col has pvalue.
			pcut is the pvalue cutoff to be less than '''
		(rest,pval) = peak.rstrip().rsplit("\t",1) 
		
		if float(pval) < float(pcut):
			return True
				
		return False

	def filter_by_existence(self,peaks1,peaks2):
		''' filters any peaks that don't exist in both interval lists'''
		
		common = list()
		for peak1 in peaks1:
			int1 = peak1.rstrip().split("\t")
			
			for peak2 in peaks2:
				int2 = peak2.rstrip().split("\t")
				
				if int1[0] == int2[1] and int1[1] == int2[0]:
					keep_str = int1[0]+"\t"+int1[1]+"\t"+int1[-1]+"\t"+int2[-1]
					
					common.append(keep_str)
					break
					
		return common
