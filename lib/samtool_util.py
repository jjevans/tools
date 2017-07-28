import os
import pysam
import subprocess

class Use():
	'''     
	Class to perform actions to alignment files with samtools.
	'''

	def __init__(self):
		pass
 
 	def sort_sam(self,samfile):
 		''' samtools sort by converting sam to bam to then sort '''
 		tmpbam = samfile + ".tmp.bam"
 		
 		self.sam_to_bam(samfile,tmpbam)
 		
 		bamfile = self.sort_bam(tmpbam,samfile)
 		
 		os.remove(tmpbam)
 		
 		return bamfile
 		
	def sort_bam(self,bamfile,outprefix):
		''' samtools sort '''
		pysam.sort(bamfile,outprefix)
		
		return outprefix + ".bam"
		
	def sam_to_bam(self,samfile,bamfile):
		''' samtools view -bS '''
		bamout = pysam.view('-bS',samfile)
		
	 	with open(bamfile,'w') as handle:
	 		handle.write("".join(bamout))
	 		
	 	return

	def sam_to_uncompress(self,samfile,bamfile):
		''' sam format to uncompressed bam format '''
		
		''' check to see if this works right!!! '''
		subprocess.check_call(["samtools","view","-u","-S",samfile,"-o",bamfile])
		
		return
		
	def merge_bam(self,outbam,inbam1,inbam2):
		''' does not work '''
		#args = ",".join(inbams)
		#print ",".join(*args)
		pysam.merge(outbam,inbam1,inbam2)

		return

	def clean_sam(self,samfile,cleanfile,path_to_picard):
		''' uses subprocess to call picard's CleanSam.jar '''
		
		#cmd = ["java","-jar",path_to_picard+"/CleanSam.jar","INPUT="+samfile,"OUTPUT="+cleanfile]
		cmd = "java -jar "+path_to_picard+"/CleanSam.jar INPUT="+samfile+" OUTPUT="+cleanfile
		
		subprocess.check_call([cmd],shell=True)
		
		return
		
	def rm_dup(self,inbam,outbam):
		''' remove pcr duplicates '''
		pysam.rmdup(inbam,outbam)
		
		return
		
	def index(self,inbam,outindex):
		''' create bam index '''
		pysam.index(inbam,outindex)
		
		return
		