import vcf

#parse and format ExAC exome data


class Vcf(Record):
	#base class
	
	def __init__(self,file):
		#input exac raw vcf (direct download)
		self.file = file
		
		try:
			self.fh = open(self.file,'r')
		except:
			message = 'Cannot open inputted VCF file: '+self.file+'\n'
			raise Exception(message)
		
		self.reader = vcf.Reader(self.fh)


	def _tags(self):
		#return list of all INFO tag names
		return

	def _values(self,tags=None):
		#filter info columns to list of tag names
		#input is a list of tag name strings as seen 
		# in header of vcf INFO definitions
		#returns a list of values for those tags in 
		# same order		
		vals = list()
		return vals
	
	'''	
	def readline(self):
		#return next vcf line
		return self.reader.next()
	'''
	
	def fields(self,tags):
		#get all INFO fields with tag name in passed in list
		return

	def close(self,files=list()):
		#close open vcf filehandle and any files 
		# from a passed in list of filenames
		if not self.exac.closed:
			close(self.exac_fh)

		return

class Record(Info):
	#for one single vcf line whether wide/long form (mutiallelic or multi-line-per-location
	
	def uniquify(self,record,delimiter=':'):
		#returns a list of strings for all variants 
		#each variant string is unique having 
		# chrom,pos,ref,alt delimited. 
		#optionally pass in delimiter
		#ex. chr=1, pos=100, ref=A, alt=[G,GC] 
		#	== ('1-100-A-G','1-100-A-C')	
		variants = list()

		#make uniq
		for alt in record.ALT:
			variants.append(delimiter.join([record.CHROM, record.POS, record.REF, alt]))

		return variants


class Info():
	#for a record set of INFO fields by tag name and field value
	#based on pyvcf record (record.INFO var)
	
	def has_tag(self, rec_info, tag):
		#boolean if tag exists in this record's info
		return rec_info.has_key(tag)
		
	def tags(self,rec_info):
		#returns a list of tags found in this record's INFO
		return rec_info.keys()
		
	def vals(self,rec_info):
		return rec_info.values()
		
	def val(self,rec_info, tag):
		#return the value for a specific INFO field tag
		#input is a INFO dict (pyvcf) and a tag name
		self.field(rec_info, tag)
		
		
		#	return rec_info[tag]
		
		return None

	def fields(self,rec_info, tags=None):
		#return tuples of all INFO fields (name, value)
		#optional list of tags to return otherwise all
		#skips tag when not in INFO dict
		view = rec_info.viewitems()
		
		if tags is not None:
			#get only these fields
			return view & tags
	
		return view

	def field(self,rec_info, tag):
		#return a tuple (tag name, value) for 
		# a INFO dict and a tag name
		if tag in rec_info:
			return tag, rec_info[tag]
		
		return None
	