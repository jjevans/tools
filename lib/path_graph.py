import rpy2.robjects as rob

####
# query for pathway graph and save to xgmml
####
# Jason Evans, 05232012
# Oliver Hofmann
# Harvard School of Public Health
####

class Use():

	def __init__(self):
		self.graph_obj = Interface_R()
		
	def graph_by_name(self,db,name):	
		self.graph_obj._define_db(db)
		
		return self.graph_obj._query_graph(name)
 		
	def save_xgmml(self,graph,filebase):
		self.graph_obj._save_xgmml(graph,filebase)
		return
		
class Interface_R():

	def __init__(self):
		self.db = None
		
		rob.r.library("graphite")
		rob.r.library("BioNet")

	def _define_db(self,db):
		self.db = db
		return
		
	def _query_graph(self,path):
		print path
		qry = self.db+"[['"+path+"']]"
		path_frame = rob.r(qry)
		
		graph = rob.r.pathwayGraph(path_frame)
		
		return graph
		
	def _save_xgmml(self,graph,filebase):
		graph_name = "jasonevans"
			
		#rob.r.suppressMessages(rob.r.saveNetwork(network=graph,file=filebase, name=graph_name, type="XGMML"))
		rob.r.saveNetwork(network=graph,file=filebase, name=graph_name, type="XGMML")
		
		return
