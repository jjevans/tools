import MySQLdb as mysql

# query hpo database for phenos based on omim/umls

class Query():

	def __init__(self,db,username,hostname):
		self.db = mysql.connect(db=db,user=username,host=hostname)
		self.curs = self.db.cursor()
		
	def ask(self,query):
		self.curs.execute(query)
		return self.curs.fetchall()
	
class HPO():

	def __init__(self,db="hpo0",username="python",hostname="localhost"):
		self.db = Query(db,username,hostname)

	def pheno_by_omim(self,omimid):
		query = '''select t.acc,t.name,eo.external_id 
				from term t, external_object eo, annotation an 
				where eo.id = an.external_object_disease_id 
				and t.id = an.term_id and eo.external_id = '''+str(omimid)

		return self.db.ask(query)		

	def pheno_by_umls(self,cuid):
		query = '''select t.acc,t.name,eo.external_id 
				from external_object eo, term2external_object t2eo, term t 
				where eo.id=t2eo.external_object_id 
				and t2eo.term_id=t.id 
				and t.is_obsolete=0 
				and eo.external_id = "'''+cuid+'"'

		return self.db.ask(query)
		
	def print_ans(self,answer):
		for ans in answer:
			for col in ans:
				print str(col),
			print
			
		return
