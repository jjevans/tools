import MySQLdb as mysql

# query umls database for cuid and omim ids

class Query():

	def __init__(self,db,username,hostname):
		self.db = mysql.connect(db=db,user=username,host=hostname)
		self.curs = self.db.cursor()
		
	def ask(self,query):
		self.curs.execute(query)
		return self.curs.fetchall()
	
class UMLS():

	def __init__(self,db="umls",username="python",hostname="localhost"):
		self.db = Query(db,username,hostname)

	def cuid_by_omim(self,omimid):
		query = '''select distinct cui from mrsat where code = "'''+str(omimid)+'"'

		return self.db.ask(query)		

	def omim_by_cuid(self,cuid):
		query = '''select distinct code from mrsat where code is not null and sab = 'OMIM' and cui = "'''+cuid+'"'
		
		return self.db.ask(query)
		
	def snomed_by_cuid(self,cuid):
		query = '''select distinct code from mrsat where code is not null and sab = 'SNOMEDCT' and cui = "'''+cuid+'"'
		
		return self.db.ask(query)
		
	def print_ans(self,answer):
		for ans in answer:
			for col in ans:
				print str(col),
			print
			
		return
