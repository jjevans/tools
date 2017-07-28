import os

#utility library to work with sequence

''' NGS '''
class SplitFile():
	''' split fastq files into multiple smaller fastqs.
		splits sam file based on number of aligns per file, 
		chunk fastq to multiple files by lines or 
		buffer (needs fix) '''

	def __init__(self,num_entry,lineperentry=4):
		self.num = int(num_entry)
		self.lineperentry = lineperentry
		
	def split_fastq(self,fastq):
		'''iterate through fastq file, create multiple files of num_seq sequences per'''
		''' change to include a buffer size in open and just write each line to buffer 
			instead of loading into list '''
			
		files = list()
		numfile = 0
		entry = list()
		seq = list()
		
		outfile = self.make_filename(fastq,numfile)
		with open(fastq) as handle:
			
			if not os.path.isfile(outfile):
				numfile += 1
			else:
				for line in handle:
					entry.append(line)
				
					if len(entry) % self.lineperseq == 0:
						seq.extend(entry)
						entry = list()
					
					if len(seq)/self.lineperentry == self.num:
						outfile = self.make_filename(fastq,numfile)
					
						with open(outfile,'w') as splitfile:
							for item in seq:
								splitfile.write(item)
						
						seq = list()
						numfile += 1
						files.append(outfile)
			
		if len(seq) != 0:
			outfile = self.make_filename(fastq,numfile)
			
			with open(outfile,'w') as splitfile:
				for item in seq:
					splitfile.write(item)
			
			files.append(outfile)
				
		return files

	def make_filename(self,fastq,numfile):
		return fastq + "." + str(numfile) + ".fastq"
	
	''' INCOMPLETE !!! '''
	'''
	def chunk_fastq_buffer(self,fastq,numfile,noclobber=False):
		
		
		files = list()
		
		filesize = os.stat(fastq)/numfile
		
		with open(fastq) as handle:
			
		seq = self.chunk(handle,filesize)
			
			
	def chunk(self,handle,num_byte):
		#takes a filehandle and a number of bytes wanted of it from its current pointer
		#reads up to the next newline and returns that piece as a string

		chunk = handle.read(num_byte)
		
		byte = str()
		while byte != "\n":
			byte = handle.read(1)
			chunk += byte
			
		return chunk
	'''
	
	def split_fastq_buffer(self,fastq,buff_len=1000000,noclobber=False):
		'''iterate through fastq file, create multiple files of num_seq sequences per'''
		''' change to include a buffer size in open and just write each line to buffer 
			instead of loading into list '''
			
		files = list()

		with open(fastq) as handle:
			
			numfile = 0
			numline = 0
		
			outfile = fastq + "." + str(numfile) + ".fastq"
			out_handle = self.open_write(outfile,buff_len,noclobber)
			files.append(outfile)

			for line in handle:
				
				if numline/self.lineperentry == self.num:
					
					self.close_handle(out_handle)
					numfile += 1
					
					outfile = fastq + "." + str(numfile) + ".fastq"
					out_handle = self.open_write(outfile,buff_len,noclobber)

					files.append(outfile)
					
					numline = 0
				
				self.write_line(out_handle,line)

				numline += 1
			
			self.close_handle(out_handle) # close handle if still open
				
		return files
		
	def write_line(self,handle,line):
		''' write the list to an output filehandle '''
		
		# only write if the filehandle exists
		if handle is not None:
			handle.write(line)
		
		return
			
	def open_write(self,filename,buff_len=0,noclobber=False):
		# defaults to no buffer (0), clobbers file by default
		
		if noclobber and os.path.exists(filename):
			return None
			
		try:
			handle = open(filename,'w',buff_len)
		except IOError:
			print "Cannot open file for write at seq_util.open_write: " + filename
			
		return handle
			
	def close_handle(self,handle):
		if handle is not None:
			try: handle.close()
			except: pass
			
		return

"""

''' !!!needs implementing '''
''' finding, locating, chunking, comparing sequence '''
class Find(Base):
        ''' locate sequence features, subseq,
                simple align (sliding window) '''

        def __init__(self,seq=None):
                self.seq = seq

        def pos(self,query):
                '''find position of a query seq, subseq '''
                pass


''' !!!needs implementing '''
class Base():
        ''' iterate, divide, sliding window '''

        def __init__(self,seq=None):
                self.seq = seq

        def slide(self):
                ''' iterate over sequence '''
                pass

        def subseq(self,pos,len):
                ''' return subsequence from seq,
                        position, length '''
                pass

        def subseqs(self,len,overlap):
                ''' return list of subsequences based
                        on length and overlab '''
                pass
"""

