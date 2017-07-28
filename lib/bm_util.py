import xml.etree.ElementTree as et
import requests as req

# biomart utilities

''' EXAMPLE XML QUERY STRING
xml = """<!DOCTYPE Query><Query client="webbrowser" processor="TSV" limit="-1" header="1">
		<Dataset name="hsapiens_gene_ensembl" config="gene_ensembl_config_4">
			<Filter name="ensembl_gene_id" value="ENSG00000139618"/>
			<Attribute name="ensembl_gene_id"/>
			<Attribute name="external_gene_id"/>
			<Attribute name="chromosome_name"/>
			<Attribute name="start_position"/>
			<Attribute name="end_position"/>
			<Attribute name="strand"/>
			<Attribute name="band"/>
			<Attribute name="transcript_count"/>
			<Attribute name="gene_biotype"/>
			<Attribute name="status"/>
		</Dataset>
	</Query>"""
'''


class Ask():

	def __init__(self,url="http://www.biomart.org/biomart/martservice"):
		self.url = url # biomart web service url
		
		self.pars = dict()
			
	def get_req(self,xml):
		# xml is the built xml query
		self.pars["query"] = xml

		try:
			response = req.get(self.url,params=self.pars).text

		except ValueError:
			response = None

		return response


class XML():
	# form query xml
	
	def __init__(self,formatter="TSV",limit="-1",header=False,client="PCPGM",vsn=None):
		# tab delimited response, no limit to num rows returned, 
		# no header, this clients name (whatever you want)
		# virtualSchemaName (need to look into) is "default" perhaps
		
		if header is True:
			putheader = "1"
		else:
			putheader = "0"

		attributes = {"formatter":formatter,"limit":limit,"header":putheader,"client":client}

		# virtualSchemaName
		if vsn is not None:
			attributes["virtualSchemaName"] = vsn

		self.tree = et.Element("Query",attrib=attributes)
		
	def dataset(self,name,config=None,interface=None):
		# add a dataset to return from response
		# subelement of the query tree

		attributes = {"name":name}
		
		if config is not None:
			attributes["config"] = config

		if interface is not None:
			attributes["interface"] = interface
		
		return et.SubElement(self.tree,"Dataset",attrib=attributes)

	def add_filter(self,dataset,name,value):
		# add the filters
		# (the ids to query for, the genome to use, etc)
		# input is the dataset produced as a subelement of the query 
		# and the name and value for the biomart filter
		
		attributes = {"name":name,"value":value}
		
		return et.SubElement(dataset,"Filter",attrib=attributes)
	
	def add_attributes(self,dataset,names):
		# add list of attributes to a dataset
		# if adding just one attribute simply use 
		# method below "add_attribute". 
		# Input is a dataset and a list 
		# of attribute names
		
		for name in names:
			self.add_attribute(dataset,name)
			
		return

	def add_attribute(self,dataset,name):
		# a biomart attribute (not xml attribute)
		# (the name of the information wanted back, 
		# like ids, coords or whatever querying for)
		# input is the dataset produced as a subelement of the query 
		# and the name of the attribute
		return et.SubElement(dataset,"Attribute",attrib={"name":name})
		
	def tostring(self):
		# xml tree tostring
		return et.tostring(self.tree)
		

class ENSG():
	# ensembl gene

#	def __init__(self,url="http://www.biomart.org/biomart/martservice"):
	def __init__(self,url="http://central.biomart.org/martservice"):

		# every method must create an xml object, cannot do in constructor!
		self.url = url
		
		# dataset and config, may always work, but not sure
		self.db = "hsapiens_gene_ensembl"
		#self.db = "gene_ensembl"
		
		# I dont think needed, self.config = "gene_ensembl_config_4"
		#self.config = "gene_ensembl_config_1"

		# object to perform web service
		self.ask_obj = Ask(url=self.url)

	def info_by_id(self,ids,header=False):
		# get gene info by ensg id(s)
		# multiple ids separated by comma
		
		attribute_names = ["ensembl_gene_id",\
						#"external_gene_id",\
						"chromosome_name",\
						"start_position",\
						"end_position",\
						"strand",\
						"band",\
						"transcript_count",\
						"gene_biotype",\
						"status"]
						
		# create query tree with dataset, id filter, and attributes to get back
		xml_obj = XML(header=header)
		dataset = xml_obj.dataset(self.db)
		xml_obj.add_filter(dataset,name="ensembl_gene_id",value=ids)		
		xml_obj.add_attributes(dataset,names=attribute_names)

		xml = xml_obj.tostring()

		return self.ask_obj.get_req(xml=xml)

	def exon_by_id(self,ids,header=False):
		# get the exon coordinates for a comma 
		# separated list of ensg ids
		
		attribute_names = ["ensembl_gene_id",\
						"ensembl_transcript_id",\
						"exon_chrom_start",\
						"exon_chrom_end",\
						"is_constitutive",\
						"rank",\
						"ensembl_exon_id",\
						"genomic_coding_start",\
						"genomic_coding_end",\
						"phase",\
						"cdna_coding_start",\
						"cdna_coding_end",\
						"cds_start",\
						"cds_end"]
						
		# create query tree with dataset, id filter, and attributes to get back
		xml_obj = XML(header=header,vsn="default")
		dataset = xml_obj.dataset(name=self.db,interface="default")
		xml_obj.add_filter(dataset,name="ensembl_gene_id",value=ids)		
		xml_obj.add_attributes(dataset,names=attribute_names)

		xml = xml_obj.tostring()
		
		return self.ask_obj.get_req(xml=xml)

"""
class Coordinate():
	#actions with a genomic coordinate
		def __init__(self,url="http://central.biomart.org/martservice"):

		# every method must create an xml object, cannot do in constructor!
		self.url = url
		
		# dataset and config, may always work, but not sure
		self.db = "hsapiens_gene_ensembl"
		#self.db = "gene_ensembl"
		
		# I dont think needed, self.config = "gene_ensembl_config_4"
		#self.config = "gene_ensembl_config_1"

		# object to perform web service
		self.ask_obj = Ask(url=self.url)

	#def __init__(self,chr,start,stop,strand=None):
	def gene_by_coord(self,chr,start,stop,strand=None):
		#get the gene for a certain location
		return
"""		
		
		
		
			
"""	!!!NEED TO COMPLETE.  CHANGE EACH OF DIFF ATTRIBS (THINGS YOU WANT)

class Convert():
	#id converters

	def __init__(self,url="http://central.biomart.org/converter/#!/ID_converter/gene_ensembl_config_2"):
		# every method must create an xml object, cannot do in constructor!
		self.url = url
		
		# dataset and config, may always work, but not sure
		self.db = "hsapiens_gene_ensembl"
		# I dont think needed, self.config = "gene_ensembl_config_2"
		
		# object to perform web service
		self.ask_obj = Ask(url=self.url)

	def enst_to_nm(self,ids,header=False):
		#convert id: ensembl transcript id to 
		# a refseq transcript id
		#input is list of ENST ids
		#returns a list of refseq ids
		
		attribute_names = ["ensembl_transcript_id","refseq_mrna"]
		
		xml_obj = XML(header=header,vsn="default")
		dataset = xml_obj.dataset(name=self.db,interface="default")
		xml_obj.add_filter(dataset,name="ensembl_gene_id",value=ids)		
		xml_obj.add_attributes(dataset,names=attribute_names)

		xml = xml_obj.tostring()
		
		return self.ask_obj.get_req(xml=xml)

	def enst_to_np(self,ids,header=False):
		#convert id: ensembl transcript id to 
		# a refseq protein id
		#input is list of ENST ids
		#returns a list of refseq protein ids
		
		attribute_names = ["ensembl_transcript_id","refseq_peptide"]

		xml_obj = XML(header=header,vsn="default")
		dataset = xml_obj.dataset(name=self.db,interface="default")
		xml_obj.add_filter(dataset,name="ensembl_gene_id",value=ids)		
		xml_obj.add_attributes(dataset,names=attribute_names)

		xml = xml_obj.tostring()
		
		return self.ask_obj.get_req(xml=xml)
	
	def enst_to_entrez(self,ids,header=False):
		#convert id: ensembl transcript id to 
		# a entrez gene id
		#input is list of ENST ids
		#returns a list of refseq ids
		
		attribute_names = ["ensembl_transcript_id","entrezgene"]

		xml_obj = XML(header=header,vsn="default")
		dataset = xml_obj.dataset(name=self.db,interface="default")
		xml_obj.add_filter(dataset,name="ensembl_gene_id",value=ids)		
		xml_obj.add_attributes(dataset,names=attribute_names)

		xml = xml_obj.tostring()
		
		return self.ask_obj.get_req(xml=xml)

	def enst_to_sym(self,ids,header=False):
		#convert id: ensembl transcript id to 
		# a hgnc gene symbol
		#input is list of ENST ids
		#returns a list of hgnc symbols
		
		attribute_names = ["ensembl_transcript_id","hgnc_symbol"]

		xml_obj = XML(header=header,vsn="default")
		dataset = xml_obj.dataset(name=self.db,interface="default")
		xml_obj.add_filter(dataset,name="ensembl_gene_id",value=ids)		
		xml_obj.add_attributes(dataset,names=attribute_names)

		xml = xml_obj.tostring()
		
		return self.ask_obj.get_req(xml=xml)

	def enst_to_uniprot(self,ids,header=False):
		#convert id: ensembl transcript id to 
		# a uniprot id
		#input is list of ENST ids
		#returns a list of uniprot ids
		
		attribute_names = ["ensembl_transcript_id","uniprot_swissprot"]
	
		xml_obj = XML(header=header,vsn="default")
		dataset = xml_obj.dataset(name=self.db,interface="default")
		xml_obj.add_filter(dataset,name="ensembl_gene_id",value=ids)		
		xml_obj.add_attributes(dataset,names=attribute_names)

		xml = xml_obj.tostring()
		
		return self.ask_obj.get_req(xml=xml)
	
	def enst_to_uniprot_acc(self,ids,header=False):
		#convert id: ensembl transcript id to 
		# a refseq transcript id
		#input is list of ENST ids
		#returns a list of refseq ids
		
		attribute_names = ["ensembl_transcript_id","uniprot_swissprot_accession"]
		
		xml_obj = XML(header=header,vsn="default")
		dataset = xml_obj.dataset(name=self.db,interface="default")
		xml_obj.add_filter(dataset,name="ensembl_gene_id",value=ids)		
		xml_obj.add_attributes(dataset,names=attribute_names)

		xml = xml_obj.tostring()
		
		return self.ask_obj.get_req(xml=xml)
"""
