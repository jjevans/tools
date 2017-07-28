import os
import paramiko
import pwd

# connect and execute commands on a remote machine

####
# Jason Evans
# Partners Center for Personalized Genetic Medicine (PCPGM)
# Partners Healthcare
####

class Link():

	def __init__(self,machine,user=None,password=None):
	
		self.args = {"hostname":machine,"username":user,"password":password}
		
		#if user is not None:
		#	self.args["username"] = user
						
		self.client = paramiko.SSHClient()
		self.client.load_system_host_keys()
		
	def connect(self):
		# connect to remote machine
		
		try:
			self.client.connect(**self.args)
		except:
			raise RemoteMachineError("Unable to connect to remote machine (paramiko).")

		return
		
	def disconnect(self):
		# disconnect from remote machine
		self.client.close()
		
		return

	def is_localhost(self,machine):
		# find if the machine name specified to run alamut on is 
		# the current machine (hostname or an alias).
		# returns True if alamut machine is the localhost
		names = list()
			
		names.append(socket.gethostname)
			
		# add aliases
		names.append(socket.gethostbyaddr(socket.gethostbyname(names[0]))[1])
			
		if machine not in names:
			return False
				
		return True

class SSH():

	def __init__(self,link_obj=None,machine=None,user=None,password=None):
		# uses a paramiko Linked client to execute unix commands, 
		# pass in a Link() object or a remote machine name and the 
		# Link() object will be made here.  if a Link() client exists,
		# bypasses any machine name passed in
		# user is ignored if current user has established ssh keys to machine
		
		if link_obj is None:
			# get username if not provided
			if user is None:
				user = pwd.getpwuid(os.getuid())[0]
				
			link_obj = Link(machine,user,password)
			
		link_obj.connect()
		
		self.client = link_obj.client			

	def execute(self,command):
		# execute an ssh command, raise exception on error
		# command is a unix command to do on remote machine	
		input,output,error = self.client.exec_command(command)		
		
		err = self.error_check(error)
		
		if err[0]:
			raise RemoteMachineError(err[1])

		return output.read().rstrip()
				
	def executes(self,commands):
		# execute a series of unix commands passed in as a list
		# returns a list of tuples of command,output
		
		outputs = list()
		for command in commands:
			output_str = self.execute(command)
			outputs.append((command,output_str))
			
		return outputs

	def execute_no_exception(self,command):
		# execute an ssh command, return exception instead of raising
		# command is a unix command to do on remote machine
		# returns a tuple of the output as 1st position and the 
		# error string, if present, as the second position. If there 
		# is no error, second position returned is None
		input,output,error = self.client.exec_command(command)
		
		# tuple of output str, None (replaced by error str if present)
		response = output.read().rstrip(),None
		
		err = self.error_check(error)
			
		return output.read().rstrip(),err[1]

	def error_check(self,ChannelStderrFile):
		# checks error output from exec_command (ChannelStderrFile) 
		# returns tuple of boolean error present or not and error 
		# string or None if present or not
		
		err_str = ChannelStderrFile.read().rstrip()
				
		if len(err_str) != 0:
			return True,err_str

		return False,None

class SFTP():

	def __init__(self,machine=None,link_obj=None,user=None,password=None):
		# uses a paramiko Linked client to execute unix commands, 
		# pass in a Link() object or a remote machine name and the 
		# Link() object will be made here.  if a Link() client exists,
		# bypasses any machine name passed in, user and password optional either way
		# constructor further takes client to open and sftp Linkion to use

		if link_obj is None:
			# get username if not provided
			if user is None:
				user = pwd.getpwuid(os.getuid())[0]
				
			link_obj = Link(machine,user,password)

		link_obj.connect()
		
		self.client = link_obj.client
		
		self.sftp = self.client.open_sftp()

	def close(self):
		# close the sftp session
		return self.sftp.close()

	def get(self,remotepath,localpath=None):
		# get a file from remotepath to a local machine's directory and filename (localpath).
		# localpath is optional and will drop the file in the cwd as same filename
		# returns True on success
		
		args = {"remotepath":remotepath}
		
		if localpath is None:
			args["localpath"] = os.getcwd()+"/"+os.path.basename(remotepath)
		else:
			args["localpath"] = localpath
			
		try:
			response = self.sftp.get(**args)
		except IOError as ioe:
			err_str = "(Remote Machine) I/O error("+str(ioe.errno)+"): "+ioe.strerror+", file from: "+remotepath+" transferring it to: "+args["localpath"]
			raise RemoteMachineError(err_str)
		except:
			err_str = "Cannot get remote file: "+remotepath+" transferring it to: "+args["localpath"]
			raise RemoteMachineError(err_str)
	
		return True

	def put(self,localpath,remotepath=None,remote_attributes=False):
		# put a file from localpath to a remote machine's directory and filename (remotepath).
		# remotepath is optional and will drop the file in the cwd as same filename
		# returns True on success, if remote_attributes arg is True, returns a string 
		# of remote machines file attributes (default False)
		
		args = {"localpath":localpath}
		
		if remotepath is None:
			args["remotepath"] = self.sftp.getcwd()+"/"+os.path.basename(localpath)
		else:
			args["remotepath"] = remotepath
			
		try:
			response = self.sftp.put(**args)
		except OSError:
			err_str = "(Local Machine) No such file or directory: "+localpath
			raise RemoteMachineError(err_str)
		except IOError as ioe:
			err_str = "(Remote Machine) I/O error("+str(ioe.errno)+"): "+ioe.strerror
			raise RemoteMachineError(err_str)
		except:
			err_str = "Cannot put local file from: "+localpath+" to remote machine location: "+args["remotepath"]
			raise RemoteMachineError(err_str)

		if remote_attributes:
			return str(response)
			
		return True
	
	def stat(self,file):
		# return the statistics of a file
		
		try:
			response = self.sftp.stat(file)
		except:
			raise RemoteMachineError("No such file: "+file)
			
		return response

	def listdir(self,directory="."):
		# return the contents of the remote path for the remote machine
		return self.sftp.listdir(path=directory)

	def chdir(self,directory):
		# change directory to the inputted directory path
		
		try:
			response = self.sftp.chdir(directory)
		except:
			raise RemoteMachineError("Cannot change directory to: "+directory)
		
		return response
		
	def mkdir(self,directory):
		# create the directory.
		
		try:
			response = self.sftp.mkdir(directory)
		except:
			raise RemoteMachineError("Cannot create directory: "+directory)
			
		return response

	def mkdir_recursively(self,newdir):
		# create the directory recursively.
		# from a directory path, starting with the most root directory 
		# and going to the least directory, create the directories 
		# that do not already exist

		dirlst = newdir.lstrip("/").rstrip("/").split("/")
		
		dirbld = str()
		for directory in dirlst:
			dirbld += "/"+directory
			
			try: # directory can be stat
				self.sftp.listdir(path=dirbld)
			except:
				self.sftp.mkdir(dirbld)

		return

	def remove(self,filepath):
		# remove the file with the path filepath
		return self.sftp.remove(filepath)
	
	
class RemoteMachineError(Exception):
	def __init__(self,probstr):
		Exception.__init__(self,probstr)
