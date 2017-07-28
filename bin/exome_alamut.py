#!/usr/bin/env python
import alamut_util
import sys
import yaml
#also requires lib remote_machine if remote

#run alamut-ht for wgs/exome annotation

'''
may be run locally or remotely as an option
config is a yaml formatted file with the 
 first level having the key "Alamut".
ex. from exome anno_conf.yml
Alamut:
  run_remote: false #run on cluster or remotely on alamut vm, true/false
  ssh: #unused if run_remote is false
    machine: alamut-ht1.dipr.partners.org
    user: nva_user #null if current user or ssh key
    password: null
    directory: /tmp #remote run directory
  executable: "/scratch/pcpgm/share/software/alamut/alamut-ht-1.1.11-standalone/alamut-ht"
  cleanup: true #remove alamut output files
  options:
      - alltrans
      - nonnsplice
      - nomispred
      - outputannonly

 if to run remotely, run_remotely must be true and ssh 
 credentials provided.  if "cleanup" is true, removes 
 the alamut output files once the output of this script 
 is created (vcf).
 options is a list of options to put on the alamut-ht 
 command-line
'''

try:
	vcf = sys.argv[1]
	out = sys.argv[2]
	log = sys.argv[3]
	config = sys.argv[4]
except:
	print "usage: exome_alamut.py input_vcf output_table(ann) output_log(unann) config_file"
	exit(0)

with open(config) as handle:
	try:
		settings = yaml.load(handle.read())
	except:
		raise Exception("Cannot read yaml config file.")


#create appropriate alamut object as to local/remote run
if settings["Alamut"]["run_remote"]:#remote run,!!!connection broken!!!
	alamut_obj = alamut_util.RemoteAlamut(**settings["Alamut"])
else:
	alamut_obj = alamut_util.Alamut(**settings["Alamut"])
	

response = alamut_obj.run_alamut(vcf=vcf,out=out,log=log)

if response[1] != str():#errors
	raise Exception("Error running alamut-ht: "+response[1])
	
#process output


exit(0)
