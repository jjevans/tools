import datetime
import copy
import io
import os
import pybedtools as pbt
import re
import subprocess
import sys

#in case of fetchChromSizes (connect to ucsc) imports in method below

#lib to run and parse bedtools

class Bedtools():
	#bedtools core options and info
	
	def __init__(self, a=None, b=None, do_clean=True, gbuild='hg19', chrom_sizes=None, stream=False):
		#chrom_sizes unused but intended as a list of tuples with chrom and length
		# these sizes are obtained via the UCSC script for the supplied genome build
		# for each chromosome or by default the name of the script 
		# that will fetch them from ucsc.  only needed for window maker
		#option to pass 0, 1, or 2 files (bam/bed) as args a and b
		#if have to fetchChromSizes (ucsc) (no bedfile provided), goes to 
		#ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/chromInfo.txt.gz
		#keep track and cleanup and tmpfiles produced
		self.tmpfiles = list()
		self.do_clean = do_clean
		self.stream = stream
		
		self.gbuild = gbuild
		self.chrom_sizes = chrom_sizes
		
		#url to get chromosome lengths from UCSC
		urlparts = '/goldenPath','database/chromInfo.txt.gz'
		self.ssh = {'host':'hgdownload.cse.ucsc.edu','path':None,'urlparts':urlparts}

		#bed/bam files
		# 1st
		self.a = a
		if a is None:
			self.bt_a = None
		else:
			self.bt_a = self.bed(self.a)

		# 2nd
		self.b = b
		if b is None:
			self.bt_b = None
		else:
			self.bt_b = self.bed(self.b)

	def bed(self,file):
		#read bedfile file or string into BedTool obj
		from_string = False 

		#if not os.path.exists(file):
		#	from_string = True

		return pbt.BedTool(file,from_string=from_string)

	def pair(self, a, b):
		#init two files (bed, bam, ...)
		# return tuple of a-BedTool and b-BedTool
		self.a = a
		self.bt_a = self.bed(self.a)
		
		self.b = b
		self.bt_b = self.bed(self.b)
		
		return self.bt_a, self.bt_b
	
	def write(self,file):
		#write bed output to file (from self.result)
		with open(file,'w') as handle:
			for item in self.result:
				handle.write(item)
				
		return
	
	def cleanup(self,do_die=True):
		#delete list of tmpfiles
		#returns any that can't be removed

		if not self.do_clean:#specified not to clean up tmpfiles
			return None
	
		for file in self.tmpfiles:
			
			try:
				os.remove(file)
				del file
			except:
				message = "ERROR: could not remove temporary file: "+file
				
				if do_die:#die on error
					raise Exception(message)

				else:#warn only
					sys.stderr.write(message)

		if len(self.tmpfiles) == 0:#successful
			return True
			
		return self.tmpfiles#remainders

	def sort(self, bt_a, sort_by=None, print_head=False):
		#sorts by coordinate, 
		#input is a BedTools obj
		#returns sorted bedtools obj
		#sort_by is the bedtools sort option 
		# (sizeA, sizeD, chrThenSizeA, chrThenSizeD, chrThenScoreA, chrThenScoreD)
		args = {print_head:print_head}
		
		if sort_by is not None:
			args[sort_by] = True
		
		return bt_a.sort(**args)

	def _cleanup(self,filelst,do_die=True):
		#delete list of files

		for file in filelst:

			try:
				os.remove(file)
				del file
			except:
				message = "ERROR: could not remove temporary file: "+file
				
				if do_die:#die on error
					raise Exception(message)

				else:#warn only
					sys.stderr.write(message)

	def fetchChromSizes(self, gbuild='hg19', host=None, path=None):
		#mimic ucsc fetchChromSizes to 
		# get the lengths of a reference genome 
		# (bed intervals over entire genome)
		#i think it... returns a BedTools object where start = 1, 
		# and stop = length chrom
		#!imports lib ssh_util!
		import ssh_util		

		#return if done previously (stored in self)
		if self.chrom_sizes is None:
	
			#work out remote file path
			if path is None:
				self.ssh['path'] = self.get_url()
			else:
				self.ssh['path'] = path


			#get remote machine or die
			if host is not None:
				self.ssh['host'] = host
				
			else:
				if self.ssh['host'] is None:
					message = 'No proper remote machine to goldenpath available.  Please provide a machine if using entire genome as intervals'
					raise Exception(message)

				else:#connect goldenpath
					ucsc_obj = ssh_util.SFTP(machine=self.ssh['host'])
					self.chrom_sizes = self.goldenpath()

		return self.chrom_sizes

	def goldenpath(self, gbuild=None):
		#build ucsc remote file path for fetchChromSizes
		#optional gbuild as arg trumps constructor
		if gbuild is not None:
			self.gbuild = gbuild

		path = self.urlparts[0]+"/"+self.gbuild+"/"+self.urlparts[1]
		
		self.ssh['path'] = path
			
		return path

	def _name_tmpfile(self):
		#returns a timestamp and .txt extension 
		# for a temporary file
		currtime = datetime.strftime(datetime.now)
		
		return str(currtime)+".tmp.txt"
	
		return filelst					
	
	def _get_arg(self,arg0=None,arg1=None):
		#test if arg0 exists and return it
		#otherwise if arg1 exists return that,
		#if niether return None
		retval = None

		if arg0 is not None:#1st arg
			retval = arg0

		elif arg1 is not None:#2nd arg
			retval = arg1

		else:#niether
			retval = None
			
		return retval
		
		
class Interval():
	#wraps BedTool Interval
	
	def init(self, **kwargs):
		self.interval = kwargs.get('interval', None)
		self.chrom = kwargs.get('chrom', None)
		self.start = kwargs.get('start', None)
		self.stop = kwargs.get('stop', None)
		self.score = kwargs.get('score', 0)
		self.strand = kwargs.get('strand', '+')
		self.otherfields = kwargs.get('otherfields', None)

		#build Interval if none provided and chrom, start provided
		if self.interval is None and self.chrom is not None and self.start is not None:
				
			if self.stop is None:
				self.stop = self.start + 1

			#create interval from chrom start stop
#			kwargs = {	'chrom':self.chrom, 'start':self.start, \
#						'stop':self.stop, 'score':self.score, \
#						'strand':self.strand, 'otherfields':self.otherfields}
				
			#create Interval
			self.interval = self._build()

		#make coord if interval or None
		self.coord = self._coord()
	
	def cp(self,intrvl):
		#deep copy an interval object
		return copy.deepcopy(intrvl)

	def _coord(self):
		#get bed coordinate and 
		# return it in format "chr:start-stop"
		#from a BedTool Interval
		#stop coord if chrom, start found
		if self.chrom is not None and self.start is not None:
		
			#single bp
			if self.stop is None:
				self.stop = start + 1

		else:
			return None
			
		return self.chrom+":"+self.start+"-"+self.stop

	def chrom(self):
		#return chr from an interval
		return self.interval.chrom
		
	def start(self,value=None):
		#return start pos from an interval
		return self.interval.start
		
	def stop(self,value=None):
		#return stop pos from an interval
		return self.interval.stop

	def count(self,value=None):
		#return count value from a bigBed interval
		return self.interval.count

	def length(self,interval):
		#return length of interval
		return self.interval.length
		
	def score(self,interval):
		#return score (col5) of interval
		return self.interval.score

	def _build(self):
		#create and return BedTool Interval obj
		#requires chrom, start, and optional stop
		#if no stop, assumes one bp like vcf

		#make Interval is chrom, start
		if self.chrom is not None and self.start is not None:
		
			if self.stop is None:#only one position if no stop
				self.stop = self.start

			args = {'chrom':self.chrom, 'start':self.start, 'stop':self.stop, \
					'score':self.score, 'strand':self.strand, 'otherfields':self.otherfields}

			return pbt.Interval(**args)

		return None

class Coverage(Bedtools):
	#use "bedtools coverage"
	# init abam and b bedfile (optional, or 
	#entire genome), optional "split" (default True)
	#requires bam file

	def __init__(self, abam=None, b=None, result=None, split=True, d=True, threshold="15,30,45,60,90,120,150,200,300,400,500,1000", gbuild='hg19', chrom_sizes=None, stream=True, add_0=True):
		#requires a bam file and a bedfile
		#binstr is comma separated string of cutoffs
		#g is a file of chromosome sizes chrom<tab>length<tab>unused_3rd_col<nl>
		self.abam = abam
		self.b = b
		self.result = result
		self.split = split
		self.d = d
		self.stream = stream
		
		self.bt_mrg = Merge(col=5, fx='collapse')
		
		#threshold cutoffs
		self.cuts = map(int, threshold.split(","))
		self.bins = list()

		# add 0 cutoff option if no 0 present
		self.add_0 = add_0
		if add_0 and self.cuts[0] != 0:
			self.cuts.insert(0,0)

		#bam
		if abam is None:
			self.bt_a = None
		else:
			self.bt_a = self.bed(abam)

		#bedfile, parse get lengths		
		if b is None:
			self.bt_b = None
			self.flens = None
		else:
			self.bt_b = self.bed(self.b)
			self.flens = self._flens()
			

		#unused
		self.gbuild = gbuild #unused, genome build to get chromosome sizes
		self.chrom_sizes = chrom_sizes #unused, output of ucsc fetchChromSizes query

		'''
		#unprovided bed so do entire genome (get chrom lengths)
		if self.b is None:
			self.bt_b = None

			#get genome sizes unless list of chr lengths provided
			self.chrom_sizes = self.fetchChromSizes(self.gbuild)

		'''

	def run(self):
		#runs bedtools, sets self.result and returns BedTool obj
		#optional arg to stream or run whole thing (default) and return all results
		#returns a bt cov obj to iterate over
		#for now only runs with -split and -d specified providing a bedgraph format
		#args = {'b':self.bt_b, 'split':self.split, 'd':self.d, 'stream':self.stream}

	
		#no input files, die
		if self.bt_b is None or self.bt_a is None:
			message = 'not enough files, requires bed and bam file to run coverage.'
			raise Exception(message)
		
		args = {'b':self.bt_b, 'split':True, 'd':True, 'stream':self.stream}

		self.result = self.bt_a.coverage(**args)
		print self.result
		'''
		#either supplied bed intervals or entire genome chromosome sizes
		if self.bt_b is None:#no bedfile
			
			if self.chrom_sizes is None:#no bed, no chrom sizes, die
				message = 'Must provide interval lengths for genome if no bedfile supplied, run fetchChromSizes()'
				raise Exception(message)
				
			args['g'] = self.chrom_sizes
		
		else:
			args['b'] = self.bt_b
		'''
			
		return


	def bin(self):
		#bin coverage counts at each position 
		# find num positions with cov count 
		# between each cutoff
		#requires a bedtools cov object in self to iterate over
		#returns a 2-d table with counts for 
		# each interval over each bin
		tallied = list()

		if self.result is None:#no coverage run
			message = "ERROR: no bedtools coverage iterator in constructor.  Please run coverage first."
			raise Exception(message)

		#collapse bed
		collapse = self._collapse(self.result)

		for intrvl in collapse:
			tallied.append(self._tally_bin(intrvl.score))

		return tallied
		

	def over(self):
		#tally coverage counts at each position 
		# that exceed the thresholds
		#find num positions with cov count 
		# between each cutoff
		#requires a bedtools cov object in self to iterate over
		#returns a 2-d table with counts for 
		# each bin over each interval

		if self.result is None:#no coverage run
			message = "ERROR: no bedtools coverage iterator in constructor.  Please run coverage first."
			raise Exception(message)

		#collapse bed
		collapse = self._collapse(self.result)

		for intrvl in collapse:
			tallied.append(self._tally_over(intrvl.score))

		return tallied
		
	def _tally_over(self, covstr):
		#tally all values over thresholds
		#input is string of values to tally 
		# self.cuts has thresholds to evaluate
		#covstr is a comma delimited string 
		# (such as that of bt merge collapse)
		#returns a list of tallies over each bin
	
		#tallies
		counts = [0] * (len(self.cuts)-1)

		#each basepair in the interval
		for bp in self.result:

			#each bin
			for i in range(0,len(self.cuts)-1):
				
				#count is between two bins so increment
				if bp.count > self.cuts[i]:
					counts[i] += 1
		
		return counts
	
	def _tally_bin(self, covstr):
		#tally all values between thresholds
		#input is string of values to tally 
		# self.cuts has thresholds to evaluate
		#covstr is a comma delimited string 
		# (such as that of bt merge collapse)
		#returns a list of tallies between each bin
		
		#tallies
		counts = [0] * (len(self.cuts)-1)

		#each basepair in the interval
		for bp in self.result:

			#each bin
			for i in range(0,len(self.cuts)-1):
				
				#count is between two bins so increment
				if self.cuts[i] <= bp.count < self.cuts[i+1]:
					counts[i] += 1
		
		return counts

	def _collapse(self, result):
		#bedtools merge (collapse) all intervals 
		# in the coverage output
		#input is output of bedtools coverage -d -split
		return self.bt_mrg.run(result)
	
			
	def avg(self):
		#averages coverage over each base of interval from bt 
		# coverage output -split, -d
		#self.result must exist
		return
		
	def cov_arr(self, collapsed):
		#collapsed is the bt coverage output bt merged with collapsed scores
		# bt merge collapsed
		
		return

	def _flens(self):
		#return a list of all interval lengths in the bed file
		flens = list()
		
		try:#if yes/no bedfile defined
			for f in self.bt_b:
				flens.append(f.length)
		except:
			message = "no bedfile defined."
			raise Exception(message)
	
		return flens


class Mkwin(Bedtools):
	def __init__(self, b=None, w=2500, s=None, i='srcwinnum', stream=True):
		#optional bedfile to break into wins (default all hg19), 
		# w=window size s=step size (no overlap), 
		# a w of 100 and s of 90 = 10bp overlap of each window
		#optional stream results instead of buffering
		#i refers to the bedtools -i option for how ids are outputted
		self.stream = stream
		self.i = i
		
		#input source	
		self.b = b
		if self.b is None:
			self.bt_b = None
		
		else:
			self.bt_b = self.bed(b)

		#winsize and step length
		self.w = w #win size
			
		if s is None:#step
			self.s = self.w
		else:
			self.s = s

	def windows(self):
		#needs self.bt_a to exist, don't get why need to pass b again
		#return self.bt_b.window_maker(b=self.b,w=self.w,s=self.s, i=self.i)
		args = {'b':self.bt_b,'w':self.w, 's':self.s, 'i':self.i}
		
		return self.bt_b.window_maker(**args)

	def equal_parts(self):
		#UNIMPLEMENTED
		#break into an equal number of windows of same size		
		return 


class GenomeCov(Bedtools):
	def __init__(self):
		pass
		
	def run_gcov(self):
		return


class Merge(Bedtools):
	#bedtools merge.  merge all intervals in one or two files

	def __init__(self, col=None, fx='collapse', stream=True):
		#requires 1 bedfile, a 2nd bedfile will be merged together
		#data is the column with the interesting data (col 5 in bed6)
		#func is a function to run on that column (default concat all 1 line)
		self.stream = stream
		self.result = None

		#files
		#self.b = b
		#self.bt_b = None
		
		#if self.b is not None:
		#	self.bt_b = self.bed(self.b)
		
		#set up data function
		self.c = None
		self.fx = None

		if col is not None:
			self.c = col
			self.fx = fx


	def run(self, bt_i=None):
		#needs self.bt_a to exist, don't get why need to pass b again
	
		#die if no bedfile
		if bt_i is None:
			message = 'no bedfile to merge'
			raise Exception(message)

		bt_arg = {'stream':self.stream}
		
		if self.c is not None:#function on column
			bt_arg['c'] = self.c
			bt_arg['o'] = self.fx
		
		try:
			return bt_i.merge(**bt_arg)
		except:
			message = 'error running bedtools merge'
			raise Exception(message)

		return


class Windows(Bedtools):
	#makewindows, combine multiple windows, assembly
	def __init__(self, b):
		self.b = b
	
	def run_makewin(self):
		return
		
class Cluster(Bedtools):
	def __init__(self):
		pass
	def run_cluster(self):
		return

class Order(Bedtools):
	def __init__(self):
		pass
	def run_sort(self):
		return
	def run_group(self):
		return




			

	'''
	def fetchChromSizes(self, outfile="chrom.sizes", script="fetchChromSizes", throw=True):
		#runs syscall of UCSC's fetchChromSizes script
		# run via a pipe and write to file
		#input is optional outfile (default chrom.sizes, cwd) 
		# and optionally the path to ucsc script if not in PATH
		#throw is boo to say whether throw exception or just return non-zero 
		# status to calling method (default throws error)
		
		with open(outfile,'w') as handle:
			sys_obj = subprocess.Popen(script,stdout=handle,shell=True)
			
		if status != 0 and throw is True:
			raise Exception("ERROR: bt_util.fetchChromSizes returned non-zero! ...terminating.")
			
		return status
	'''

