#!/usr/bin/env python
import subprocess
import yaml

##jje, 10282014
#use a yaml string of error handling values 
# and build shell script to run using trap
#output to stdout, no input

def get_yml():
	return yaml.load('''
Cleanup:
  enable:
    trap: true
    email: true
    execute: true
    rmfile: false
  email:
    address:
      - "jevans16@partners.org"
      #- "etsai3@partners.org"
    subject: "ERROR1 - Process failed. varAnno.pl"
    body: "ERROR2 - There was a problem running variantAnnotation.pl due to..."
  execute:
    - "echo 'ERROR3 - Problem echoed to log as a cleanup measure. VariantAnnotation.pl...'"
    - "export DATE=`date`"
    - "echo $DATE"
    - "echo LOG MESSAGE $DATE > junk.oktodel.log"
    - "du -h ~ | head"
    - "echo FAIL!!!"''')


def build_trap():
	conf = get_yml()

	##cleanup function if fail
	outstr = None #outstr is a shell script if enabled, None otherwise
	
	#required to enable any of Cleanup sections
	if conf["Cleanup"]["enable"]["trap"]:
		
		outstr = "\n\nfunction handle_err {\n\n"
		
		#send email
		if conf["Cleanup"]["enable"]["email"]:
			addresses = ",".join(conf["Cleanup"]["email"]["address"])
			outstr += "echo '"+conf["Cleanup"]["email"]["body"]+"' | mail -s traptest '"+addresses+"'\n\n"


		#execute these commands
		if conf["Cleanup"]["enable"]["execute"]:
			outstr += "\n".join(conf["Cleanup"]["execute"])+"\n\n"
		
		
		#remove files or other maintenance			
		if conf["Cleanup"]["enable"]["rmfile"]:
			outstr += "rm "+"\nrm ".join(conf["Cleanup"]["rmfile"])+"\n\n"
		
		
		outstr += "}\n\ntrap handle_err EXIT\n"
		
	return outstr


#run		
if __name__ == '__main__':
	
	main_cmds = "#!/usr/bin/env sh\nls -lrt ~ | head\necho ellen in da haus!\nls -lrt ~/nonexistent_file\n"
	print main_cmds
	
	output = build_trap()
	if output is not None:
		print output
	
	exit(0)


