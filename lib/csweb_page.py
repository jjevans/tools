import json
from mako.template import Template

######
#	generate html and javascript for embedding Cytoscape Web
#	using mako to template
######
#	Jason Evans 01122012
#	Oliver Hofmann
#	Bioinformatics Core
#	Harvard School of Public Health
######
######	

class Page_Gen():
	''' combine network with mako template to produce html '''

	def __init__(self,plate,net,sty,anno):
	
		# template filename, network, json object of visual styles
		plate_obj = Template(filename=plate)
		
		self.html = plate_obj.render(network=net, style=sty, annotation=anno)
		
	def debug(self,filepath):
		print filepath
		return filepath
	