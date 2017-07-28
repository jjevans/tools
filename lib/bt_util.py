import datetime
import os
import pybedtools
import re
import subprocess
import sys

#in case of fetchChromSizes (connect to ucsc) imports in method below

#lib to run and parse bedtools

class Bedtools():
	#bedtools core options and info
	
	def __init__(self,a=None,b=None,do_clean=True,gbuild='hg19',gsize=None):
		#chrsize is optional list of tuples with chrom and length 
		# for each chromosome or by default the name of the script 
		# that will fetch them from ucsc.  only needed for window maker
		#option to pass 0, 1, or 2 files (bam/bed) as args a and b
		#if have to fetchChromSizes (ucsc), goes to 
		#ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/chromInfo.txt.gz
		#keep track and cleanup and tmpfiles produced
		self.tmpfiles = list()
		self.do_clean = do_clean

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
		
		#store genome sizes if done
		self.gsize = gsize

	def bed(self,file):
		#read bedfile file into BedTool obj
		return pybedtools.BedTool(file)

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
	
	def fetchChromSizes(self,gbuild=None,rmchr=True,machine=None,path=None):
		#mimic ucsc fetchChromSizes to 
		# get the lengths of a reference genome 
		# (bedfile of entire genome)
		#returns a BedTools object where start = 1, 
		# and stop = length chrom
		#optional arg rmchr indicates to remove 
		# leading "chr" (ucsc) or None (ncbi), 
		# default None, !imports lib ssh_util!
		import ssh_util

		#re for lead chr even if unused
		if rmchr:
			pattern = re.compile('^chr')
		

		#return if done previously (stored in self)
		if self.gsize is not None:
			return self.gsize
		
		#arg genome trumps genome build in constructor
		if gbuild is not None:
			self.gbuild = gbuild

		#work out remote file path
		if path is None:
			self.ssh['path'] = self.get_url()
		else:
			self.ssh['path'] = path

		#remote machine
		if machine is not None:
			self.ssh['machine'] = machine


		#retrieve file
		ucsc_obj = ssh_util.SFTP(machine=self.ssh['machine'])
		dl_fh = ucsc_obj.get(self.ssh['path'])

		#rm chr (if set) and write sizes to file chr<tab>length<tab>remote_file(optional)<nl>
		tmpfile = self._name_tmpfile()
		with open(tmpfile,'w') as handle:
	
			for chrsize in dl_fh:#chromosome size line
				
				if rmchr:
					col = chrsize.split('\t')
					
					pattern.sub(col[0])
					
					chrsize = '\t'.join(col)
		
				handle.write(chrsize)
		
		#track tempfile
		self.tmpfiles.append(tmpfile)
		
		return tmpfile
		
	def goldenpath(self,gbuild=None):
		#build ucsc remote file path for fetchChromSizes

		if gbuild is None:
			gbuild = self.gbuild
		
		path = self.urlparts[0]+"/"+gbuild+"/"+self.urlparts[1]
		
		self.ssh['path'] = path

		return path
		
	def _name_tmpfile(self):
		#returns a timestamp and .txt extension 
		# for a temporary file
		currtime = datetime.strftime(datetime.now)
		
		return str(currtime)+".tmp.txt"
	
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
		if self.chrom is not None and self.start is not None and self.stop is not None:

			kwargs = {'chrom':self.chrom, 'start':self.start, 'stop':self.stop, \
					'score':self.score, 'strand':self.strand, 'otherfields':self.otherfields}

		else:#no coords provided to make interval
			return None

		return pybedtools.Interval(**kwargs)


class Coverage(Bedtools):
	#use "bedtools coverage"
	# init abam and b bedfile (optional, or 
	#entire genome), optional "split" (default True)
	#requires bam file

	def __init__(self,abam, b=None, split=True, d=True, binstr="15,30,45,60,90,120,150,200,300,400,500,1000", g=None, stream=True):
		#requires a bam file and a bedfile
		#binstr is comma separated string of cutoffs
		#g is a file of chromosome sizes chrom<tab>length<tab>unused_3rd_col<nl>
		self.abam = abam
		self.b = b
		self.split = split
		self.d = d
		self.g = g #genome sizes file
		self.stream = stream
		
		#should i keep all results in object or keep it clean?
		self.result = None

		#bam
		self.bt_a = self.bed(abam)

		#unprovided bed so do entire genome (get chrom lengths)
		if self.b is None:
			self.bt_b = None

			#get genome sizes unless file of chr lengths provided
			if self.g is None:
				self.g = self.fetchChromSizes(self.gbuild)

		else:
			self.bt_b = self.bed(self.b)


		#bins list of int cutoffs
		self.bins = map(int, binstr.split(","))
		
		#add 0 cutoff unless exists
		if self.bins[0] != 0:
			self.bins.insert(0,0)


	def run(self):
		#runs bedtools, sets self.result and returns BedTool obj
		#optional arg to stream or run whole thing and return all results
		#returns a bt cov obj to iterate over
		
		args = {'split':self.split,'d':self.d,'stream':self.stream}
		if self.bt_b is None:
			args['g'] = self.g
		else:
			args['b'] = self.bt_b
		self.bt_iter = self.bt_a.coverage(b=self.bt_b, split=self.split, d=self.d, stream=stream)

		return self.bt_iter

	def bin(self,bt_iter=None):
		#bin coverage counts at each position 
		# find num positions with cov count 
		# between each cutoff
		#requires a bedtools cov object to iterate over
		#returns a 2-d table with counts for 
		# each bin over each interval

		#find bedtools iterator and reassign in construct
		self.bt_iter = self._get_arg(bt_iter,self.bt_iter)
		
		if self.bt_iter is None:#bt iter not in arg or constructor
			message = "ERROR: no bedtools coverage iterator object passed in or in self.bt_iter"
			raise Exception(message)

		#tally
		counts = [0] * (len(self.bins)-1)

		#each basepair in the interval
		for bp in self.bt_iter:

			#each bin
			for i in range(0,len(self.bins)-1):
				
				#count is between two bins so increment
				if self.bins[i] <= bp.count < self.bins[i+1]:
					counts[i]+=1
		
		return counts

	def over(self,bt_iter=None):
		#tally num bases over each cutoff 
		#ex answers how many bases are over 30X?
		#requires a bedtools cov object to iterate over
		# either as arg or in self.bt_iter
		
		#find bedtools iterator
		#reassign in construct
		self.bt_iter = self._get_arg(bt_iter,self.bt_iter)
		
		if self.bt_iter is None:

			message = "ERROR: no bedtools coverage iterator object passed in or in self.bt_iter"
			raise Exception(message)
				
		#tally
		counts = [0] * (len(self.bins))
		
		for bp in self.bt_iter:
			print bp.chrom+" "+bp.start+" "+bp.stop+" "+bp.count
			#each bin
			for i, bin in enumerate(self.bins):
				if bp.count > bin:
					count[i]+=1
					
		return counts
	
		'''careful, goes outside this method		
	def stream_func(self, func_name, func_args=dict()):
		#runs bt coverage, pipes to function (optionally) 
		#returns list of result lines (raw or after through function
		results = list()

		#add trailing parens if not present
		func = self.str_to_func(func_name)

		#process
		covs = self.bt_a.coverage(b=self.bt_b, split=self.split, d=self.d, stream=True)
		print str(**func_args)
		for cov in covs:
			#run function for each interval
			result = eval(func,**func_args)
			
			results.push(result)
			
		return results


	def str_to_func(self, func):
		#takes a string name of a function and 
		# adds "()" to end to make an official function
		if re.search("\(\)$",func) is None:
			func += "()"
	
		if re.search("^self\.",func) is None:
			func = "self."+func
		print func
		return func

	def avg_cov(self,interval):
		#use results to get average coverage over interval
		print self.coord(interval)+" yo"
		
		return
	'''

		return counts

class Mkwin(Bedtools):
	def __init__(self, b=None, w=2500, s=None, n=None):
		#needs bedfile, w=window size s=step size (no overlap)
		# a w of 100 and s of 90 = 10bp overlap of each window
	
		self.b = b
		if b is None:
			self.bt_b = None
		else:
			self.bt_b = self.bed(b)
	
		#win size
		self.w = w
		
		#step size
		if s is None:
			self.s = w
		else:
			self.s = s			
		self.s = self.s
		
	def windows(self):
		#needs self.bt_a to exist, don't get why need to pass b again
		return self.bt_b.window_maker(b=self.b,w=self.w,s=self.s)

class GenomeCov(Bedtools):
	def __init__(self):
		pass
		
	def run_gcov(self):
		return

class Merge(Bedtools):
	#bedtools merge.  merge all intervals in one or two files
	def __init__(self, a, b=None, datacol=5, func='sum'):
		#requires 1 bedfile, a 2nd bedfile will be merged together
		#datacol is the column with the interesting data (col 5 in bed6)
		#func is a function to run on that column (default unique values)
		self.a = a
		self.bt_a = self.bed(self.a)
		
		self.b = b

		if self.b is None:#make bt obj if 2nd file provided
			self.bt_b = None
		
		else:
			self.bt_b = self.bed(self.b)
		
		if b is None:
			self.bt_b = None
		else:
			self.bt_b = self.bed(b)
	
		#win size
		self.w = w
		
		#step size
		if s is None:
			self.s = w
		else:
			self.s = s			
		self.s = self.s
		
	def run(self):
		#needs self.bt_a to exist, don't get why need to pass b again
		return self.bt_a.merge(b=self.b,w=self.w,s=self.s)

class Utilities():
	#little helper methods and tools such as sort bed
	
	def sort(self, bt_a):
		#sorts by coordinate, 
		#input is either a BedTools obj
		#returns sorted bedtools obj
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
	def window_maker(self,chrsize=None,winsize=500,olapsize=0,numwin=None):
		#break an interval into a series of sub-intervals (windows)
		#input is a BedTool Interval obj, a file of chromosome sizes 
		# (from ucsc fetchChromSizes) and optionally a window size 
		# and overlap size.  if num_win defined, winsize and overlap ignored 
		# and it is split into num_win equally lengthed intervals
 
 		if chrsize is None and self.chrsize is None:
 			raise Exception("ERROR: requires chromosome sizes file/script to make windows.\n Use script (UCSC) fetchChromSizes\n")
		else:
			#temporary file
 			tmpfile = self._name_tmpfile()
			self.tmpfiles.append(tmpfile)
 			
 			#get chromosome sizes if no file provided
			self.fetchChromSizes(outfile=tmpfile)
 		
 		return
	'''

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


'''
my $delim = "|";
my $binstr_default = "15,30,45,60,90,120,150,200,300,400,500,1000";
my $binstr;
my $noheader;
my $addcut;
my $bin;#truebin
my $infile;
my $outfile;


##run vals
my $bt_arg = {"i"=>\$infile,
			  "o"=>\$outfile,
			  "cut"=>\$binstr,
			  "noheader"=>\$noheader,
			  "addcut"=>\$addcut,
			  "bin"=>\$bin};

GetOptions($bt_arg,"i=s","o=s","cut|c=s","noheader|nh","addcut","bin|b");
#print Data::Dumper->Dump(${$bt_arg->{"i"}});

#usage
if(-t *STDIN && !defined(${$bt_arg->{"i"}})){#requires either stdin or file or die
	die "usage: bt_cov_bin.pl -i input file -bin thresholds -o output file (default stdout)\n\
			-i input file (default stdin)\
			-o output file (default stdout)\
			-cut,c comma delimited list of thresholds (default 15,30,45,60,90,120,150,200,300,400,500,1000)\
			-noheader,nh print header (default prints)\
			-addcut add threshold coverage in each cell separated by delimiter\
			-bin,b report read frequency between each threshold\
		#input file optional though requires either input on stdin or specified file\
		#default reports all reads over that threshold\
		#use bin option report all read frequencies between the two thresholds\n"; 
}


##input, stdin or inputted file
my $in_fh;
if(defined(${$bt_arg->{"i"}})){
	open($in_fh,${$bt_arg->{"i"}}) || die "Cannot open input file: ".${$bt_arg->{"i"}}."\n";
}
else{
	$in_fh = \*STDIN;
}


##bins, defaults (above) or input string by comma
my @cuts;
if(defined(${$bt_arg->{"cut"}})){
	@cuts = split(/\,/,${$bt_arg->{"cut"}});
}
else{
	@cuts = split(/\,/,$binstr_default);
}
unshift(@cuts,0) unless $cuts[0] == 0;#add 0 bin

##count each bp
my $prev;#previous interval location

my $num_0 = 0;#count of bp under 1st bin val

my @lines = <$in_fh>;

my @col = split(/\t/,$lines[0]);
my $len = abs($col[2]-$col[1]);

my @freqs = (0) x @cuts;

my @outs;

for(my $i=0;$i<@lines;$i++){
	$lines[$i] =~ s/\n$//;

	#my($chr,$start,$stop,$rel_pos,$cov) = split(/\t/,$lines[$i]);
	my @col = split(/\t/,$lines[$i]);
	my $chr = $col[0];
	my $start = $col[1];
	my $stop = $col[2];
	my $cov = $col[-1];
	
	my $coord=$chr.":::".$start.":::".$stop;#unique

	#transition to new interval
 	if($prev ne $coord && $i != 0){#next interval

		#output line
		my @loc = split(/:::/,$prev);
		
		if(defined($addcut)){#add threshold to frequency sep by delim
			for(my $x=0;$x<@freqs;$x++){
				$freqs[$x] = $cuts[$x].$delim.$freqs[$x];
			}
		}	
			
		my $outstr = join("\t",@loc)."\t".$len."\t".join("\t",@freqs);	
		push(@outs,$outstr);
		
		$len = abs($stop-$start);

		@freqs = (0) x @cuts;
	}

	#tally each bin
	for(my $j=0;$j<@cuts;$j++){#skip coord cols
		
		if($cov > $cuts[$j]){
			
			if(defined(${$bt_arg->{"bin"}})){#bin between thresholds
				$freqs[$j]++ if ($j == @cuts-1 || $cov <= $cuts[($j+1)]);
			}			
			else{#bin over thresholds
				$freqs[$j]++;
			}
		}
	}
	
	$prev = $coord;
}

#output final interval
my @loc = split(/:::/,$prev);

my $outstr = join("\t",@loc)."\t".$len."\t".join("\t",@freqs);
push(@outs,$outstr);


##output, stdout or output file
my $out_fh;
if(defined(${$bt_arg->{"o"}})){

	open($out_fh,">${$bt_arg->{'o'}}") || die "Cannot open output file: ".${$bt_arg->{"o"}}."\n";
}
else{
	$out_fh = \*STDOUT;
}

#print header
unless(${$bt_arg->{"noheader"}}){#optional header
	print $out_fh "#chr\tstart\tstop\tlength\t".join("\t",@cuts)."\n";
}


#print output
foreach my $out (@outs){
	print $out_fh $out."\n";
}

close($in_fh);
close($out_fh);

exit;


#numerical sort
sub number { $a<=>$b }
'''
