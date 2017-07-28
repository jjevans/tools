import json
import re
import yaml

######
#	produce networks, change attributes for Cytoscape Web API 
######
#	Jason Evans 01122012
#	Oliver Hofmann
#	Bioinformatics Core
#	Harvard School of Public Health
######
######	
class Settings():
	''' Use the yaml formatted string and organize by config attribute '''
	def __init__(self,conf_str):
		''' from configuration file in yaml '''
		anno_lbl = "annotation"
		att_lbl = "groups"
		sty_lbl = "style"
		
		raw = yaml.load(conf_str)
	
		# organize entries by the group of node/edge or other styles or the 
		# attributes to be printed to the annotation pane
		self.anno = raw[anno_lbl]
		#self.group = self._group_stys(raw[att_lbl])
		self.style = self._other_stys(raw[sty_lbl])
		
	def _group_stys(self,atts):
		# creates dict with name as key and json structure of styles as vals
		# takes yaml dictionary and the name of key to access the node names
		name_lbl = "name"
				
		# name of attribute as key and value is a list of dicts with name
		# as key and attribute value as value 
		attributes = dict()
		att_lst = list()
		for values in atts:
			
			# get group name
			name = values[name_lbl]
			# remove name of group from attributes 
			del values[name_lbl]	

			# each attribute, 
			for value in values:
				# if this att doesn't already have an entry
				if value not in attributes:
					attributes[value] = list()				
					
				attributes[value].append({name:values[value]})
		
		# map the attributes to the entries of the group
		att_lst.append(self._att_to_mapper(value,attributes))
		 	
		return att_lst
	
	def _att_to_mapper(self,label,attributes):
		''' gets attribute, adds its values as values 
	 	in a dict with the label as key, returns a list of 
	 	 attributes of dicts; label as key and a list of entries 
	 	 as values for that attribute'''

	 	att_lst = list()
		for attribute in attributes:
			entries = self._att_to_entry(attributes[attribute])
			
			entry_dict = {"attrName":label,"entries":entries}
			
			att_json = json.dumps(entry_dict)
			
			att_lst.append(att_json)
			
		return att_lst
	
	def _att_to_entry(self,attribute):
		''' produce a list of entries for the discrete mapper '''
		
		entries = list()
		for att in attribute:
			for group in att.keys():

				entry = {"attrValue":group, "value":str(att[group])}
				
				entries.append(entry)
			
		return entries

	def _other_stys(self,stys):
		
		# converts other styles into a json structure
		# takes yaml dict and name of key to access style
		#return re.sub('\"','JJE',json.dumps(stys))
		#return json.dumps(stys,ensure_ascii=False)
		return json.dumps(stys)
		
class Nets():
	''' produce networks for graph '''
	# need to use json instead of this concatenation business
	
	def __init__(self,content):
		self.net = self.form_net(content) 
		
	def tab_to_netmod(self,content):
		# convert a string in tab-delim format to its nodes and edges 
		# formatting it as a string of javascript
		nodes = dict()
		edge_str = 'edges: ['
		
		for line in content.splitlines():
			if line is "":
				continue
			else:
				cols = line.split("\t")
				
				nodes[cols[0]] = '{id: "'+cols[0]+'"},'
				nodes[cols[1]] = '{id: "'+cols[1]+'"},'			
				
				edge_str += '{source: "'+cols[0]+'", target: "'+cols[1]+'"},'
	
		edge_str = edge_str.rstrip(",")+']'
		
		node_str = 'nodes: ['+"".join(nodes.values()).rstrip(",")+']'
		
		net_str = '{data: {'+node_str+','+edge_str+'}}'
				
		return net_str		
		
	def is_xml(self,content):
		# does not work yet
		check_str = "<?xml"
		
		if check_str in content:
			return True
		
		return False

	def is_gml(self,content):
		# finds if it's graphml/xgmml or another format
		check_str = "graph"
		
		if check_str in content:
			return True
		
		return False
	
	def form_net(self,content):
	
		# XGMML or adjacency pairs
		# GML format acceptable though buggy
		if self.is_gml(content):
			# removes any single quotes in content so it doesn't 
			# interfere with the cytoscape web javascript
			network = re.sub("'","",content)
		else:
			# not in graph markup, create network module
			network = self.tab_to_netmod(content)	
		
		# get rid of unneeded whitespace, newline makes this software break
		
		return re.sub('[\n\t\s+]',' ',network)

class Styles():
	''' produce visual styles from config attribute values '''
	
	def __init__(self,style,grp_sty=None):
		pass
		
		
	def merge_sty(self):
		pass
	