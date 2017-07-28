import hgvs.parser
import hgvs.dataproviders.uta
import hgvs.variantmapper
import re

#utilities using python hgvs 
# (http://pythonhosted.org/hgvs)

class HGVS():
	#make and convert variants to and from hgvs
	
	def __init__(self,gbuild='GRCh37.p10'):
		self.gbuild = gbuild

		self.parser = hgvs.parser.Parser()

		db = hgvs.dataproviders.uta.connect()
		self.mapper = hgvs.variantmapper.VariantMapper(db)

	def make_list(self,nomlst):
		#from a list of hgvs variants (nm_001:c.271C>T) 
		# return a list of hgvs objs
		
		variants = list()
		for nom in nomlst:
			variants.append(self.make(nom))
			
		return variants
	
	def make(self,nom):
		#from hgvs variant (nm_001:c.231C>T) create hgvs obj
		
		print nom
		return self.parser.parse_hgvs_variant(nom)

	def c_to_g(self,cdot):
		#return hgvs g. obj from c. obj
		return self.mapper.c_to_g(cdot,self.gbuild)

	def c_to_gcoord(self,cdot):
		#get genomic coordinates from a c. hgvs obj
		#returns tuple chr, start, end
		gdot = self.c_to_g(cdot)
		
		return self.g_to_gcoord(gdot)

	def g_to_gcoord(self,gdot):
		#get genomic coordinates from a g. hgvs obj
		#returns tuple chr, start, end 
		chr = gdot.ac
		pos = str(gdot.posedit.pos)

		try:#interval delimited by _ if insert
			start, end = pos.split('_')
		except ValueError:
		
			if pos.find('+') >= 0:#indel doesn't have interval obj
				start = None
			else:
				start = pos
			
			end = start

		return chr, start, end
		
	def chr(self,gdot):
		return gdot.ac
		
	def start(self,gdot):
		return
	
	def ref(self,gdot):
		return gdot.posedit.edit.ref_s
		
	def alt(self,gdot):
		return gdot.posedit.edit.alt

'''
	def chr_to_nc(self,chrnum):
		#make ncbi chromesome accession (NC_000022, NC_000023) 
		# from chromosome (22 or X)
		prefix = 'NC_0000'

		if chrnum == 'X':
			chrnum = 23
		elif chrnum == 'Y':
			chrnum = 24
		
		if int(chrnum) < 10:
			prefix += '0'

		return prefix+str(chrnum)

	def nc_to_chr(self,nc):
		#make chromosome number (22 or X) from 
		# ncbi chromosome accession (NC_000022, NC_000023)
		if nc.endswith('23'):
			chr = 'X'
		elif nc.endswith('24'):
			chr = 'Y'
		else:
			chr = re.subn(nc,'0','')
			
		return nc
'''
'''
class CDOT(HGVS):
	#work with c dot (c.) hgvs nomenclature
	def __init__(self,gbuild='GRCh37.p10'):
		self.gbuild = gbuild

	def c_to_g(self,variant):
		#return hgvs g. obj from c. obj
		return self.mapper.c_to_g(variant,gbuild)
'''		
	