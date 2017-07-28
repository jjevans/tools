#!/usr/bin/env python
from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
import logging
import sys
import inspect

def submit(submitJobRequest):
	print "###MESSAGE START###"

	#if submitJobRequest is not None:
	#	print inspect.getmembers(submitJobRequest)

	logging.warning("submitJob.\n" + submitJobRequest.taskId + "\n")
	print "###MESSAGE END###"

	return submitJobRequest

def ping():
	print "###MESSAGE START###"

	#if pingRequest is not None:
	#	print inspect.getmembers(pingRequest)
	#pass
	#print "ping: "+str(args)
	logging.warning("ping.")
	print "###MESSAGE END###"
	return

def get_tasks():
	print "###MESSAGE START###"

	#pass
	#print "ping: "+str(args)
	logging.warning("getTasks.")
	print "###MESSAGE END###"

	return list

	
dispatcher = SoapDispatcher(
	'server',
	location = "http://ppm-sanger-dev.dipr.partners.org:8080/gp/services/Analysis",
	action = ('submitJob','ping','getTasks'), # SOAPAction
	trace = True,
	ns = False)

'''	#namespace = "http://ppm-sanger-dev.dipr.partners.org:8080/gp/services/Analysis?wsdl",
	namespace = "http://hive49-206.dipr.partners.org:8080/gp/services/Analysis?wsdl",'''
	
	
	
# register submitJob
#dispatcher.register_function('submitJob', echo,
#	returns={'response': dict}, 
#	args={'request': dict})

# register submitJob
dispatcher.register_function('submitJob', submit,
	returns={'submitJobResponse': list}, 
	args={'submitJobRequest': list})

# register getTasks
dispatcher.register_function('getTasks', get_tasks,
	returns={'getTasksResponse': list}, 
	args={})

# register ping
dispatcher.register_function(
	'ping', ping,
	returns={'pingResponse': str},
	args={})


httpd = HTTPServer(("",8080),SOAPHandler)
logging.warning("started server.")

httpd.dispatcher = dispatcher
httpd.serve_forever()
	
exit(0)
