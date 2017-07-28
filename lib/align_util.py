import os
import samtool_util
import subprocess

class SplitFile():
	''' split a sam file up by the number of alignments desired per file '''
	def __init__(self,samfile,num_align):
		self.file = samfile
		self.num = int(num_align)

	def split_file(self):
		'''iterate through sam file, get header, produce multiple sam files of num_align length'''
		''' if num_align inputted is 0, just return the same filename '''
		
		head = list()
		align = list()
		files = list()
		numfile = 0
		
		if self.num == 0:
			# just return original file
			files.append(self.file)
		else:
			with open(self.file) as handle:
				for line in handle:
					if line.startswith("@"):
						head.append(line)
					else:
						align.append(line)
	
					if len(align) == self.num:
						outfile = self.file + "." + str(numfile) + ".sam"
						
						headline = "".join(head)
						
						with open(outfile,'w') as splitfile:
							splitfile.write(headline)
							
							for item in align:
								splitfile.write(item)

						files.append(outfile)
						numfile += 1
						align = list()
						
			if len(align) != 0:
				outfile = self.file + "." + str(numfile) + ".sam"
				
				headline = "".join(head)
				
				with open(outfile,'w') as splitfile:
					splitfile.write(headline)
				
					for item in align:
						splitfile.write(item)
				
				files.append(outfile)
			
		return files

class Head():

	def __init__(self,samfile):
		self.file = samfile
		
	def pull_head(self):
		''' get and return the header lines from an inputted samfile, returns list '''
		headlines = list()
		
		with open(self.file) as handle:
			for line in handle:
				if line.startswith("@"):
					headlines.append(line)
				else:
					handle.seek(0,0)
					break

		return headlines
		
	def num_headlines(self):
		''' returns the total number header lines in an inputted samfile'''

		num_line = 0
		with open(self.file) as handle:
			for line in handle:
				if line.startswith("@"):
					num_line += 1
				else:
					break
					
		return num_line

class BreakFile():
	''' potentially broken!!! '''
	
	def __init__(self,samfile):
		self.file = samfile
		
		self.head_obj = Head(samfile)
		
		self.size = os.stat(self.file).st_size
		self.headsize = self.aln_begin()
		self.alnsize = self.size - self.headsize
		
		self.headlines = self.head_obj.pull_head()
		
		self.breaks = dict()
		
	def make_files(self,num_file,num_byte=1048576):
		''' num_byte is the size of chunks to iterate through, default 1Gb '''
		
		num = 0
		newfiles = list()
		
		pointers = self.break_points(num_file)
		
		with open(self.file) as orig:
	
			for begin in sorted(pointers.keys()):
				# sort keys so files are made in succession, 1st file with 1st set of align, etc.
				# not necessary, but easier to debug
				print str(begin)+" begin"
				newfile = self.file+"."+str(num)+".sam"

				with open(newfile,'w') as new:
					
					new.write("".join(self.headlines))

					orig.seek(begin,0)
					
					getlen = num_byte
					if orig.tell() + num_byte > pointers[begin]:

						getlen = pointers[begin] - orig.tell()
					
					for piece in orig.read(getlen):	
						new.write(piece)
						
						if orig.tell() + getlen > pointers[begin]:
							getlen = pointers[begin] - orig.tell()
					
					new.close()
					
					newfiles.append(newfile)
					num += 1
				print str(begin)+" "+str(pointers[begin])+" "+newfile
				
		return newfiles

	def break_points(self,num_file):
		
		chunk = int(self.alnsize/int(num_file))
		
		begin = self.headsize
		with open(self.file) as handle:
			
			while begin < self.size:
				end = self.next_nl(handle,begin+chunk)
				
				self.breaks[begin] = end
				print "begend "+str(begin)+" "+str(begin+chunk)+" "+str(end)
				
				begin = end + 1
	
		print str(self.breaks)
		return self.breaks
	
	def next_nl(self,handle,point):
		
		handle.seek(point)

		nl_pos = None
		while True:
			print str(handle.tell())
			if handle.read(1) == "\n":
				nl_pos = handle.tell()
				print str(nl_pos)
				break
			elif handle.tell() >= self.size:
				nl_pos = self.size 
				break
		
		return nl_pos

	def aln_begin(self):
		''' return the index location of the end of the header (first point of alignments) '''
		
		index = 0
		with open(self.file) as handle:

			for line in handle:
				if line.startswith("@"):
					index = index + len(line)
				if line.startswith("@") is False:
					break

		return index

class BWA():
	
	def __init__(self,prefix,thread=12):
		self.prefix = prefix
		self.thread = thread
		
	def multifastq_call(self,lefts,rights,rg,basename="paired"):

		samfiles = list()
		for i,x in enumerate(lefts):

			outsai1 = lefts[i]+".sai"
			outsai2 = rights[i]+".sai"
	
			cmdaln1 = ['bwa','aln',self.prefix,lefts[i],'-t',str(self.thread),'-f',outsai1]
			cmdaln2 = ['bwa','aln',self.prefix,rights[i],'-t',str(self.thread),'-f',outsai2]

			outsam = basename+"."+str(i)+".sam"
			cmdpe = ['bwa','sampe',self.prefix,outsai1,outsai2,lefts[i],rights[i],'-f',outsam,'-r',rg]
	
			subprocess.check_call(cmdaln1)
			subprocess.check_call(cmdaln2)
			subprocess.check_call(cmdpe)
	
			samfiles.append(outsam)

		return samfiles
	
	def multifastq_lsf(self,lsf_obj,lefts,rights,rg,basename="paired"):
			
		cmd = "bwa"
		jobids = list()
		for i,x in enumerate(lefts):
			
			cmdaln1 = ['aln',self.prefix,lefts[i],'-t',str(self.thread),'-f',lefts[i]+".sai"]
			cmdaln2 = ['aln',self.prefix,rights[i],'-t',str(self.thread),'-f',rights[i]+".sai"]

			jobids.append(lsf_obj.submit(cmd,cmdaln1))
			jobids.append(lsf_obj.submit(cmd,cmdaln2))
			
		lsf_obj.sync(jobids)	
		
		samfiles = list()
		jobids = list()
		for i,x in enumerate(lefts):
		
			outsam = basename+"."+str(i)+".sam"
		
			cmdpe = ['sampe',self.prefix,lefts[i]+".sai",rights[i]+".sai",lefts[i],rights[i],'-f',outsam,'-r',rg]
			
			jobids.append(lsf_obj.submit(cmd,cmdpe))

			samfiles.append(outsam)
			
		lsf_obj.sync(jobids)
		
		return samfiles

	
