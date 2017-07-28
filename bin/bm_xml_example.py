#!/usr/bin/env python
import requests as req

url = "http://www.biomart.org/biomart/martservice"

xml = """<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE Query>
	<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
			
	<Dataset name = "hsapiens_gene_ensembl" interface = "default" >
		<Filter name = "ensembl_gene_id" value = "ENSG00000184702,ENSG00000125354,ENSG00000122545"/>
		<Attribute name = "ensembl_gene_id" />
		<Attribute name = "ensembl_transcript_id" />
		<Attribute name = "exon_chrom_start" />
		<Attribute name = "exon_chrom_end" />
		<Attribute name = "is_constitutive" />
		<Attribute name = "rank" />
		<Attribute name = "ensembl_exon_id" />
		<Attribute name = "genomic_coding_start" />
		<Attribute name = "genomic_coding_end" />
		<Attribute name = "phase" />
		<Attribute name = "cdna_coding_start" />
		<Attribute name = "cdna_coding_end" />
		<Attribute name = "cds_start" />
		<Attribute name = "cds_end" />
	</Dataset>
	</Query>"""
	
pars = {"query":xml}

response = req.get(url,params=pars).text

print response
