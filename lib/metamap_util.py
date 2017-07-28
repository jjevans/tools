import re
import subprocess

''' run and parse metamap (nlm) for nlp query of umls '''

''' keywords, key is regex search term, value is the name of key to assign
	keywords = {
			"databases":"db",
			"table":"table",
			"Derivational":"derivational",
			"lexicon":"lexicon",
			"generation":"mode",
			"metamap":"version",
			"Control":"opt",
			"Server":"host",
			"Processing":"process",
			"Phrase":"phrase",
			"Candidates":"candidates",
			"Mapping":"mapping"} '''

''' the candidates and mappings (multiple cuids per) is a list of dictionaries.
	each dictionary has keys "cuid","score","desc" for cuid, metamap score,
	cuid description '''
				
class Query():
	
	def ask(self,phrase):
		ans = self.run_mm(phrase)
		
		self.parse_mm(ans)

		return
						
	def run_mm(self,phrase):
		cmd = "echo " + phrase + " | metamap12 -I"
		
		return subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
		
	def parse_mm(self,ans):
		# uses regular expression to find line, splits into
		# strings or lists of cuids with dict of info
		
		# these terms need to iterate on subsequent lines to get all entries
		# set to None if no results
		props = ["candidate","mapping"]
		self.fix_props(props)
		
		keywords = {
			"databases":"db",
			"table":"table",
			"Derivational":"derivational",
			"lexicon":"lexicon",
			"generation":"mode",
			"metamap":"version",
			"Control":"opt",
			"Server":"host",
			"Processing":"process",
			"Phrase":"phrase",
			"Candidates":"candidate",
			"Mapping":"mapping"}
		
		subsequent = None	
		for line in ans.split("\n"):
			val = line
			
			if subsequent is not None:

				if line.startswith(" "):
					val = self.org_by_cuid(line)
					
					existing = getattr(self,subsequent)
					existing.append(val)
					setattr(self,subsequent,existing)
				else:
					subsequent = None

			for kw in keywords:

				if re.search(kw,line):

					for prop in props:
						
						if prop == keywords[kw]:
							subsequent = keywords[kw]
							val = []
							break
					
					setattr(self,keywords[kw],val)
					
		return

	def fix_props(self,props):
		# set these properties to None if undefined
		
		for prop in props:
			try:
				getattr(self,prop)
			except:
				setattr(self,prop,None)
				
		return

	def org_by_cuid(self,line):
		# creates three keys in dictionary, "cuid","score","desc"
		
		(score,info) = line.lstrip().split(None,1)
		(cuid,desc) = info.split(":")
		
		values = dict()
		values["cuid"] = cuid
		values["score"] = score
		values["desc"] = desc
		
		return values
