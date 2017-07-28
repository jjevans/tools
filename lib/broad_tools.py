import subprocess

#lib to run broad variant tools (gatk, mutect)

#jje16 04112015
#partners personalized medicine

class Walker():
	#common class for all walkers
	#defaults to gatk, but accepts mutect
	
	self __init__(self, walker, kit='GenomeAnalysisTK.jar', input=None, output=None, ref_fa=None, interval=None, known_snp=None, known_indel=None, mem_s='2000', mem_x='4000'):
		#requires a prepared bam file sorted by coord
		self.args = None #final destination for all args of complete command
		
		#toolkit
		self.kit = kit
		self.walker = walker
		
		#I/O
		self.input = input
		self.output = output
		
		#roi bedfile
		self.interval = interval

		#references
		self.ref_fa = ref_fa
		self.known_snp = known_snp
		self.known_indel = known_indel
		
		#java mem alloc
		self.mem_s = '-Xms'+mem_s+'m'
		self.mem_x = '-Xmx'+mem_x+'m'


	def bld_args(self):
		#build args
		if self.walker is None:
			message = "No walker provided at method: bld_args()"
			raise Exception(message)

		self.arg_tool = [self.kit, '-T', self.walker]
		
		#I/O
		arg_io = list()
		if self.input is None:
			message = "No input file (bam) provided for walker: "+self.walker
			arg_io.extend(['-I', self.input])

		if self.output is None:
			message = "No output file provided for walker: "+self.walker
			raise Exception(message)
		else:
			arg_io.extend(['-o', self.output])
		
		#roi
		if self.interval is not None:
			arg_io.extend(['-targetIntervals', self.interval])
		
		self.arg_io = arg_io
		

		#references
		arg_ref = list()
		if self.ref_fa is not None:
			self.arg_ref.extend(['-R', self.ref_fa])

		#resources
		if self.known_snp is not None:
			self.arg_ref.extend(['-snp', self.known_snp])

		if self.known_indel is not None:
			self.arg_ref.extend(['-known', self.known_indel])
	
		self.arg_ref = arg_ref


		#java
		self.arg_java = ['java', '-Xms'+self.mem_s, '-Xmx'+self.mem_x, '-jar']

		#collect all arguments
		self.args = self.arg_java + self.arg_kit + self.arg_io + self.arg_ref

		return self.args


	def walk(self):
		#execute syscall
		#requires a input and output file
		args = self.bld_cmd()
		
		proc = subprocess.Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
		stdout, stderr = proc.communicate()
		
		#if stderr is not None:
		#	self.assess_err(stderr)
			
		return stdout, stderr
		
	def assess_err(self,errstr):
		#deal with stderr
		#unimplemented
		return


class Align(Walker):
	#work with bams (realign, recal)
	
	def __init__(self, input, output=None, **kwargs):
		#requires a walker name and input bam (sorted)
		self.kit = "GenomeAnalysisTK.jar"

		self.input = input

		if output is None:
			self.output = self.input+".bam"
		else:
			self.output = output

		self.arg_io = ['-I', self.bam_in, '-o', self.bam_out]
		

	def realn(self):
		#IndelRealigner
		self.walker = "IndelRealigner"

		stdout, stderr = self.walk()
		
		return stdout, stderr

	def bqsr(self):
		#BaseRecalibrator
		self.walker = "BaseRecalibrator"
		
		stdout, stderr = self.walk()
		
		return stdout, stderr
