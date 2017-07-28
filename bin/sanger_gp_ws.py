#!/usr/bin/env python
import gp
import os
import sys

#submit a job to genepattern web service
#input is a filepath to zip file
#calls task
url = "http://ppm-sanger-dev.dipr.partners.org:8080/gp"
user = "jevans16@partners.org"

#module is name or lsid
#module_id = " LMMSeqQualityRun"
module_id = "urn:lsid:8080.root.ppm-sanger-dev.ppm-sanger-dev.dipr.partners.org:genepatternmodules:3:2"

try:
	file = sys.argv[1]
except:
	print "usage: sanger_gp_ws.py zipped_file_of_.ab1"
	exit(0)

print "file: "+os.path.basename(file)

#arguments to use
arg_name = "arg0","arg1"
arg_val = file, "yoyoyo"


#connect
server = gp.GPServer(url,user,None)


#get available tasks
tasks = server.get_task_list()

for task in tasks:
	print "gp task: "+str(task.get_name())


module = tasks[1]
print "module: "+str(module.get_name())
 
 
#module args
module.param_load()
params = module.get_parameters()

for param in params:
	print "gp parameter: "+str(param.get_name())
 

#job
job_spec = module.make_job_spec()


#set parameters/args for job 
for i in xrange(len(arg_name)):
	job_spec.set_parameter(arg_name[i],arg_val[i])


#upload file
upfile = server.upload_file(file)
print upfile.get_url()
job_spec.set_parameter(file,upfile.get_url())


#run job
job = server.run_job(job_spec)

if job.is_finished():
	print str(job.get_info())
 
exit(0)
