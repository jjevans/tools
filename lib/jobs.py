import os
import signal
import subprocess
import sys
import time
from copy import deepcopy
from datetime import datetime
import time

#multiprocessing with subprocess module
#jje 01302019

class Process():
	#run a job

	def __init__(self, stdout=None, stderr=None, nt=1, sleeplength=0.5, do_print=False, do_verbose=False, do_kill=True, do_throw=True, error_code=-99, bufsize=0):
		#if killall then kill all processes with SIGTERM if any process has non-zero exit status (returncode).  will 
		#attempt to kill job again if doesn't respond up to killtries attempts
		
		self.stdout = stdout
		self.stderr = stderr
		self.nt = int(nt)#number of threads max to run concurrently

		self.sleeplen = sleeplength#length to wait between checking for job completion

		self.do_print = do_print
		self.do_verbose = do_verbose
		self.do_throw = do_throw
		self.do_kill = do_kill

		self.pids = dict()#process ids and their commands
		self.gid = None#process group id#can only be one process group then at a time

		self.errorcode = error_code

		self.bufsize = bufsize

	def run(self, cmd, stdout=None, shell=True):
		#subprocess obj Popen, communicate/call/wait 
		#returns subprocess instance
		if stdout is None:
			if self.stdout is None:
				stdout = subprocess.PIPE
			else:
				stdout = self.stdout

		if self.stderr is None:
			stderr = subprocess.PIPE
		else:
			stderr = self.stderr

		#sp = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, shell=shell, preexec_fn=os.setsid, bufsize=self.bufsize)
		sp = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, shell=shell, bufsize=self.bufsize)

		
		if self.do_print and self.do_verbose:
			print("INFO: pid: " + str(sp.pid) + "\tcmd: " + str(cmd))

		return sp

	def add_pipe(self, sp, cmd, stdout=None, stderr=None, shell=True):
		#take stdout of one process and make it stdin of subprocess made from command
		#always puts stderr to sp.PIPE.  stdout may be a file objects or subprocess.PIPE if None
		#can only run this method if subprocess object passed in has stdout of subprocess.PIPE
		if stdout is None:
			stdout = subprocess.PIPE

		if stderr is None:
			stderr = subprocess.PIPE

		#pipeline = subprocess.Popen(cmd, stdin=sp.stdout, stdout=stdout, stderr=stderr, shell=False, preexec_fn=os.setsid, bufsize=self.bufsize)
		pipeline = subprocess.Popen(cmd, stdin=sp.stdout, stdout=stdout, stderr=stderr, shell=shell, bufsize=0)
		
		sp.stdout.close()
		
		return pipeline

	def run_many(self, cmds, nt=None, outfiles=None):
		#inputted list of commands
		#run nt jobs simultaneously
		#return 0 if success, returncode error encountered.  self.pids has processes like in run_many()
		#if filenames provided files will be opened and used as stdout.  they are closed prior to sp finishing
		if outfiles is None:
			files = None
		else:
			files = deepcopy(outfiles)

		if nt is None:
			nt = self.nt
		else:
			nt = int(nt)

		if self.do_print:
			print("limit threads as close to: " + str(nt))

		if files is not None and len(cmds) != len(files):
			message = "ERROR: in jobs.Process().run_many(), number of commands not the same as the number of output filenames.  cmds: " + str(len(cmds)) + ", output files: " + str(len(files)) + "\n"
			raise Exception(message)

		processes = list()

		while 1:#submit and loop over processes until all commands complete

			numactive = 0
			for i, sp in enumerate(processes):#get process status, add new processes when others finish, update return code and output on completion, handle errors (die, kill all)
				
				if sp is not None:#skip unless an active subprocess
					status = sp.poll()

					if status is None:#still running
						numactive += 1
					
						#probably unnecessary
						if sp.stdout is not None:
							sp.stdout.flush()
						if sp.stderr is not None:
							sp.stderr.flush()

					elif self.pids[str(sp.pid)]["returncode"] is None:#finished and requires update (skip if already exists)
						res = sp.communicate()#get final outputs
					
						#timestamp and return status record
						#self.pids[str(sp.pid)]["returncode"] = sp.returncode
						self.pids[str(sp.pid)]["returncode"] = sp.returncode
						#self.pids[str(sp.pid)]["endtime"] = datetime.now().strftime("%m%d%y%H%M%S%f")
						self.pids[str(sp.pid)]["endepoch"] = time.time()
						self.pids[str(sp.pid)]["endtime"] = time.ctime(self.pids[str(sp.pid)]["endepoch"])

						#try to flush output
						'''
						if sp.stdout is not None:
							sp.stdout.flush()
						if sp.stderr is not None:
							sp.stderr.flush()
						'''
						if len(res) > 0:#has stdout

							if res[0] is None:
								outval = None
							else:#has content
								outval = "\n".join(res[0]).rstrip()	

							self.pids[str(sp.pid)]["stdout"] = res[0]
	
						if len(res) > 1:#has stderr in res
					
							if res[1] is None:
								errval = None

							else:#has content
								errval = "\n".join(res[1]).rstrip()

							self.pids[str(sp.pid)]["stderr"] = res[1]

						#ERROR
						if sp.returncode > 0:#error occurred
							if self.do_kill or self.do_throw:#error, kill rest if do_kill
								self.killall(processes)
						
							if self.do_throw:
								raise JobError(errpid=str(sp.pid), pids=self.pids, errno=sp.returncode)

							elif self.do_kill:#just return terminated jobs
								return self.errorcode#exit status

					#destroy sp since done
					processes[i] = None

			#break out when done
			if numactive == len(cmds) == 0:#exit loop
				break


			#pause between kicking off more jobs
			if self.sleeplen is not None:#sleep a moment before checking again
				time.sleep(self.sleeplen)


			#add more processes as slots open up
			while numactive < nt and len(cmds) > 0:
				cmd = cmds.pop(0)

				if files is None:
					outfile = None
					fh = None
				else:
					outfile = files.pop(0)
					fh = open(outfile, 'w')

				epochsec = time.time()

				sp = self.run(cmd, stdout=fh)

				#close file if created with open
				if fh is not None and not fh.closed:
					fh.close()

				self.pids[str(sp.pid)] = {"cmd": cmd, "pg":sp.pid, "returncode": None, "stdout": None, "stderr": None, "startepoch": epochsec, "endepoch": None, "starttime": time.ctime(epochsec), "endtime": None, "outfile": outfile}
				#self.pids[str(sp.pid)] = {"cmd": cmd, "pg":sp.pid, "returncode": None, "stdout": None, "stderr": None, "starttime": datetime.now().strftime("%m%d%y%H%M%S%f"), "endtime": None, "outfile": outfile}

				processes.append(sp)

				numactive += 1


		return 0#exit status zero

	def run_pipes(self, cmd_tups, nt=None, outfiles=None):
		#go through tuples of commands, build command pipes from each tuple in serial
		#run nt cmd pipelines concurrently
		#return 0 if success, returncode error encountered.  self.pids has processes like in run_many()
		#all stdout, stderr channelled to subprocess.PIPE
		#if outfiles is list of filenames to write to (must be same length as cmd_tups) then writes final output to files
		if outfiles is None:
			files = None
		else:
			files = deepcopy(outfiles)

		if nt is None:
			nt = self.nt
		else:
			nt = int(nt)

		if self.do_print:
			print("limit threads as close to: " + str(nt))

		if files is not None and len(cmd_tups) != len(files):
			message = "ERROR: in jobs.Process().run_pipes(), number of command tuples not the same as the number of output filenames.  cmd pipes: " + str(len(cmd_tups)) + ", output files: " + str(len(files)) + "\n"
			raise Exception(message)

		processes = list()

		while 1:#submit and loop over processes until all commands complete

			numactive = 0
			for i, sp in enumerate(processes):#get process status, add new processes when others finish, update return code and output on completion, handle errors (die, kill all)

				if sp is not None:#skip unless active subprocess
					status = sp.poll()
					
					if self.do_print and self.do_verbose:
						print("#INFO: process id: " + str(sp.pid) + "\treturn status: " + str(status) + "\tcmd: " + self.pids[str(sp.pid)]["cmd"])
	
					if status is None:#still running
						numactive += 1
	
					elif self.pids[str(sp.pid)]["returncode"] is None:#finished and requires update (skip if already exists)
						
						#flush output, close file descriptors, record output, destroy finished process
						if self.pids[str(sp.pid)]["endpoint"]:
							res = sp.communicate()
						else:
							sp.wait()
							res = list()

						#self.pids[str(sp.pid)]["returncode"] = sp.returncode
						self.pids[str(sp.pid)]["returncode"] = sp.returncode
						#self.pids[str(sp.pid)]["endtime"] = datetime.now().strftime("%m%d%y%H%M%S%f")
						self.pids[str(sp.pid)]["endepoch"] = time.time()
						self.pids[str(sp.pid)]["endtime"] = time.ctime(self.pids[str(sp.pid)]["endepoch"])

						##try to flush output
						##if "endpoint" in self.pids[str(sp.pid)] and self.pids[str(sp.pid)]["endpoint"]:#is last command in pipeline, flush
						
						#	##close filehandle if written and not sys.stdout/stderr
						#	##if "fh" in self.pids[str(sp.pid)] and self.pids[str(sp.pid)]["fh"] is not None and self.pids[str(sp.pid)]["fh"] is not sys.stdout and self.pids[str(sp.pid)]["fh"]  is not #sys.stderr:
						#	##	fh = self.pids[str(sp.pid)]["fh"]
						#	##	fh.close()

						#	##	if self.do_print:
						#	##		print "#INFO: file closed.  " + str(self.pids[str(sp.pid)]["fh"]) + "\tcmd: " + self.pids[str(sp.pid)]["cmd"]
	
						#	##	del self.pids[str(sp.pid)]["fh"]
	
	
						if len(res) > 0:#has stdout
	
							if res[0] is None:
								outval = None
							else:#has content
								outval = "\n".join(res[0]).rstrip()	
	
							self.pids[str(sp.pid)]["stdout"] = res[0]
	
						if len(res) > 1:#has stderr in res
						
							if res[1] is None:
								errval = None
	
							else:#has content
								errval = "\n".join(res[1]).rstrip()
	
							self.pids[str(sp.pid)]["stderr"] = res[1]
	
						#ERROR
						if sp.returncode > 0:#error occurred
							if self.do_kill or self.do_throw:#error, kill rest if do_kill
	
								if self.do_print:
									print("#WARN: terminating all running jobs.")
	
								self.killall(processes)
	
							if self.do_throw:
								raise JobError(errpid=str(sp.pid), pids=self.pids, errno=sp.returncode)
	
							elif self.do_kill:#just return terminated jobs
								return self.errorcode#exit status
	
						if self.do_print:
							print("#INFO: job complete: " + str(sp.pid) + "\treturn status: " + str(sp.returncode) + "\tcmd: " + self.pids[str(sp.pid)]["cmd"])


						processes[i] = None#destroy sp if done
	
			#break out when done
			if numactive == len(cmd_tups) and numactive == 0:#exit loop
				if self.do_print:
					print("#INFO: job runner complete.")
				
				break


			if self.sleeplen is not None:#sleep a moment before checking again
				time.sleep(self.sleeplen)


			if self.do_print:
				print("#INFO: active threads:" + str(numactive) + "\tremaining jobs to run: " + str(len(cmd_tups)))

			#add more processes as slots open up
			while numactive < nt and len(cmd_tups) > 0:
				cmd_tup = cmd_tups.pop(0)

				if files is not None:
					outfile = files.pop(0)

					try:
						fh = open(outfile, 'w')

					except IOError as ioe:
						message = "#ERROR: cannot open output file for write at jobs.Process().run_pipes(), file: " + str(outfile) + ", errno: " + str(ioe.errno) + ", stderr: " + str(ioe.strerr) + "\n"
						raise Exception(message)

				else:
					outfile = None
					fh = None

				if len(cmd_tup) == 1:#if only one command and outfile exists then assign it to write
					endpoint = True
					stdout = fh
				else:
					endpoint = False
					stdout = None

				epochsec = time.time()

				#create first process
				processes.append(self.run(cmd_tup[0], stdout=stdout))

				#make record of job
				self.pids[str(processes[-1].pid)] = {"cmd": cmd_tup[0], "pg":processes[-1].pid, "returncode": None, "stdout": None, "stderr": None, "endpoint": endpoint, "startepoch": epochsec, "endepoch": None, "starttime": time.ctime(epochsec), "endtime": None, "outfile": outfile if endpoint else None}
				#self.pids[str(processes[-1].pid)] = {"cmd": cmd_tup[0], "pg":processes[-1].pid, "returncode": None, "stdout": None, "stderr": None, "fh": fh, "endpoint": endpoint, "starttime": datetime.now().strftime("%m%d%y%H%M%S%f"), "endtime": None}

				numactive += 1
 
				if len(cmd_tup) > 1:#add piped commands to subprocesses
					for i, cmd in enumerate(cmd_tup[1:]):#add pipe to rest of commands

						if self.do_print:
							print("#INFO: adding command pipe #" + str(i) + "\t" + cmd)

						if i == len(cmd_tup) - 2:#assign to write to outfile only if last command
							endpoint = True
							stdout = fh
						else:
							endpoint = False
							stdout = None

						epochsec = time.time()

						processes.append(self.add_pipe(processes[-1], cmd, stdout=stdout))

						if endpoint and fh is not None and not fh.closed:#close final file descriptor
							fh.close()

						self.pids[str(processes[-1].pid)] = {"cmd": cmd, "pg":processes[-1].pid, "cmd": cmd, "returncode": None, "stdout": None, "stderr": None, "endpoint": endpoint, "startepoch": epochsec, "endepoch": None, "starttime": time.ctime(epochsec), "endtime": None, "outfile": outfile if endpoint else None}
						#self.pids[str(processes[-1].pid)] = {"cmd": cmd, "pg":processes[-1].pid, "cmd": cmd, "returncode": None, "stdout": None, "stderr": None, "fh": fh, "endpoint": endpoint, "starttime": datetime.now().strftime("%m%d%y%H%M%S%f"), "endtime": None}

						numactive += 1

		return 0#exit status zero

	def stop_pg(self, processes):#suspend processes
		for sp in processes:

			if sp.poll() is None:# and self.pids[str(sp.pid)] is True:#running

				sp.send_signal(signal.SIGSTOP)		
				#self.pids[str(sp.pid)] = False

		return

	def resume_pg(self, processes):#resume processes
		#find process group of children for this process and resume them from being stopped to continue
		#job(s) must be stopped already (SIGSTOP)
		for sp in processes:
			if sp.poll() is None:#self.pids[str(sp.pid)] is False:#stopped/suspended

				sp.send_signal(signal.SIGCONT)

		return

	def killall(self, processes):
		#send kill signal to any running processes. input is array of subprocess.Popen objects
		for sp in reversed(processes):
			if sp is not None and sp.poll() is None:#ask it to terminate
				sp.kill()#kill job

				time.sleep(0.5)
			
				self.pids[str(sp.pid)]["returncode"] = self.errorcode

				success = True if sp.poll() is not None else False#orphaned if no returncode

				self.pids[str(sp.pid)]["stderr"] = "#ERROR: A different process had a run time error and this process received a signal to terminate. pid: " + str(sp.pid) + ", sucessfully terminated: " + str(success) + "\n"
  
		return

	def collect_stderr(self, errpid=None):
		#make a string with all jobs stderr, return codes, and pids from self.pid.  if errpid defined then specifies which error propagated interrupt signals
		strerr = str()

		for pid in self.pids:
			if errpid is not None and pid == errpid:#this process caused the error that sent signal to terminate all running jobs
				strerr += "#ERROR: failed process: " + pid + ", exit status: " + str(self.pids[pid]["returncode"]) + "\nERROR: failed command: " + pid + "\tcommand: " + str(self.pids[pid]["cmd"]) + "\nERROR: failed process stderr. " + pid + "\t" + str(self.pids[pid]["stderr"])  

			else:#rest of processes run with it
				if self.pids[pid]["returncode"] == 0:
					strerr += "#INFO: process successfully completed: " + pid + ", exit status: 0, command:\t" + self.pids[pid]["cmd"] + "\n"
				else:#orphaned process
					strerr += "#ERROR: process error or interrupted: " + pid + ", exit status: " + str(self.pids[pid]["returncode"]) + ", cmd: " + self.pids[pid]["cmd"] + "\n"
					strerr += "#ERROR: process error or interrupted: " + pid + ", stderr: " + self.pids[pid]["stderr"].rstrip() + "\n"

		return strerr

class JobError(Exception):
	def __init__(self, errpid, pids=None, errno=None, strerr=None):
		#error if one of the subproceses failed.  errpid is the process id of the process having the error. errno is the error number sent to propagate
		#strerr is the error message.  pids is a dictionary of processes (key of pid).  it provides the 'returncode' and 'stdout', 'stderr', 
		self.errpid = errpid
		self.errno = errno
		self.strerr = "#ERROR: jobs.Process encountered an error with a command it was running.  pid: " + str(errpid) + "\nERROR: run time error! failed pid: " + str(errpid) + " error number: " + str(errno) + "\n"

		if pids is not None:#job info

			for pid in pids:
				if pid == errpid:#this process caused the error that sent signal to terminate all running jobs
					self.strerr += "#ERROR: failed process: " + pid + ", exit status: " + str(pids[pid]["returncode"]) + "\nERROR: failed command: " + pid + "\tcommand: " + str(pids[pid]["cmd"]) + "\nERROR: failed process stderr. " + pid + "\t" + str(pids[pid]["stderr"])  

				else:#rest of processes run with it
					if pids[pid]["returncode"] == 0:
						self.strerr += "#ERROR: process successfully completed: " + pid + ", exit status: 0, command:\t" + pids[pid]["cmd"] + "\n"
					else:#orphaned process
						self.strerr += "#ERROR: process interrupted: " + pid + ", exit status: " + str(pids[pid]["returncode"]) + ", cmd: " + pids[pid]["cmd"] + "\n"
						self.strerr += "#ERROR: process interrupted: " + pid + ", stderr: " + str(pids[pid]["stderr"]).rstrip() + "\n"

		self.strerr += "#ERROR: job(s) terminated.\n"

		Exception.__init__(self, self.strerr)
