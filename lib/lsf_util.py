import drmaa

class LSF():
	'''     
	Class to perform actions to alignment files with samtools.
	'''
	
	def __init__(self,lsfargs=None):
 		# finicky, has core dumped in initialize.  
		# inits a drmaa session.  
		# !must be done in correct order or things 
		# get squirrely.
		'''# Order: 
		#	-create this obj with/without job args 
		#	for constructor, 
		#	-if not in constructor, create jobTemplate 
		#	with self.runner()
		#	-submit
		#	-wait, release whatuva	'''
		
		self.session = drmaa.Session()
 		
 		if lsfargs is not None:
 			''' arguments passed to LSF in a string, like -q pcpgm -o outfile '''
 			self.job = self.runner(lsfargs) 			
 			
 			self.args = lsfargs
 		else:
 			self.job = None
 
 		# finicky, has core dumped in initialize.  
 		self.session.initialize()
	
	def runner(self,lsfarg=None):
		#lsfargs = dict of resource requirements,
		#	keys must be same name as the bsub 
		#	flags (key "q" translates to -q where 
		#	-q is the lsf command-line flag
		self.runner = createJobTemplate()
 
 
 		self.job.nativeSpecification = self._natSpec()
		
	def set_cmd(self,cmd=None):
		#put command to execute or lsf script 
		# to submit


		if cmd is not None:
			self.runner.remoteCommand = cmd

		return
		
	'''
		createJobTemplate()
	
	plate.remoteCommand = cmd
	plate.args = args
	
	
	job = sesh.runJob(plate)
	print "job #: "+str(job)
	
	print "waiting..."
	sesh.wait(job,drmaa.Session.TIMEOUT_WAIT_FOREVER)
	print "job complete."
	
	sesh.deleteJobTemplate(plate)
	'''	
		
 	def submit(self,cmd,cmdarg=list()):
 		''' bsub '''
 		
 		self.job.remoteCommand = cmd
 		self.job.args = cmdarg
 		self.job.joinFiles = True
 		
 		return self.session.runJob(self.job)
 		
 	def delete_job(self):
 		''' free up lsf resources once jobs submitted, lose control of job '''
 		self.session.deleteJobTemplate(self.job)
 		
 		return
 		
 	def wait(self,jobid):
 		''' wait for a single job '''
 		return self.session.wait(jobid,drmaa.Session.TIMEOUT_WAIT_FOREVER)
 		
 	def sync(self,jobids):
 		''' wait for multiple jobs, input is list of job ids '''
 		return self.session.synchronize(jobids,drmaa.Session.TIMEOUT_WAIT_FOREVER)
 		
 	def kill(self,jobid):
 		''' bkill '''
 		return self.session.control(jobid,drmaa.JobControlAction.TERMINATE)
 		
	def _natSpec(self):
		#build the nativeSpecification 
		# for resource requirement
		if self.args is not None and (self.args.n is not None or self.args.R is not None):
			spec = "'rusage["

			#memory
			if self.args.R is not None:
				spec += "mem="+self.args.R
				
			#num processors
			if self.args.n is not None and self.args.n != 1:
				spec += ",ncpus="+self.args.n+"] span[hosts=1"
	
			spec += "]'"
			
			return spec

		return None