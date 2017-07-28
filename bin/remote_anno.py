#!/usr/bin/env python
import os.path
import remote_machine
import sys
import yaml

#take an input vcf and config to submit anno job remotely
#created to run on variant annotation command on cluster
#see config for structure (initial=remote_conf.yml)


def bld_cmd(executable,args=list()):
	#build a command to execute on command line
	#input is program to run and a tuple of elements 
	# arg name (or None) and arg value. 
	#  ex (--config, conf_filename), (None, value_of_arg).
	cmd = executable
	
	#add arguments
	for arg in args:
		if arg[0] is not None:#arg name
			cmd += " "+arg[0]

		if arg[1] is not None:#arg value
			cmd += " "+str(arg[1])
			
	return cmd

def arg_to_vcf(cols):
	#take a dict with keys/vals
	# of each vcf col (see vcf_dict())
	# and return a vcf line
	default = '.'
	
	
	
	return
	
def vcf_dict():
	#return tup of 2 elems
	#1st elem is dict with keys for each vcf col
	#values of None will default value to '.'
	#2nd is list of order of keys in dict (vcf 
	# col order)
	vcf_keys = ['chr','pos','id','ref','alt','qual','filter','info']
	
	info = dict()
	
	for vcf_key in vcf_keys:
		info[vcf_key] = None
	

	#add a list for variable number samples
	info['sample'] = list()

	return info, vcf_keys


#exec
if __name__ == "__main__":
	vcf_arg = "--input_vcf"
	
	try:
		vcf = sys.argv[1]
		conf = sys.argv[2]
	except:
		print "usage: anno_remote.py vcf_file config_file"
		exit(1)


	#config
	with open(conf) as handle:
		yml_str = handle.read().rstrip()
		conf = yaml.load(yml_str)


	#vcf existence check
	if not os.path.exists(vcf):
		message = "VCF file does not exist: " + vcf
		raise Exception(message)

	#add remote location of vcf file arg (for now) to conf args
	remote_vcf = conf["Remote"]["directory"]+"/"+os.path.basename(vcf)
	conf["Execute"]["args"].append((vcf_arg, remote_vcf))
	
	#build command
	cmd = bld_cmd(conf["Execute"]["executable"], conf["Execute"]["args"])
	
	#wrap lsf
	if conf["LSF"]["executable"] is not None:
		cmd = bld_cmd(conf["LSF"]["executable"], conf["LSF"]["args"]) + " " + cmd

	print "cmd: "+cmd
	#connect to remote machine
	link_obj = remote_machine.Link(**conf["Remote"]["location"])

	#copy file over
	sftp_obj = remote_machine.SFTP(link_obj=link_obj)
	sftp_obj.put(vcf, remote_vcf)
	
	#execute command
	ssh_obj = remote_machine.SSH(link_obj=link_obj)
	ssh_obj.execute(command=cmd)


exit()
