#!/usr/bin/env perl
use strict;

#mutect vcf with normal and tumor samples both in last two columns.
#this script moves the allele depth (AD) from the normal sample column 
# removing the normal column from outputted vcf.  normal allele freq 
# is FORMAT field NAD (normal tissue allele dep from norm sample col (col[-2])).
#1st arg is name of mutect outputted vcf, prints modified vcf to stdout
#ASSUMES AD IN 2nd SAMPLE FIELD
my $nad = "NAD";#name of format field form normal's allele depth (AD in raw)
my $nad_declare =  '##FORMAT=<ID='.$nad.',Number=.,Type=Integer,Description="NORMAL tissue allelic depths for the ref and alt alleles in the order listed">';

die "usage: vcf_mutect_nad.pl mutect_outputted_vcf\n" unless @ARGV == 1;
my $vcf = $ARGV[0];

open(my $vcf_fh,$vcf) || die "Cannot open inputted vcf\n";
while(<$vcf_fh>){

	if(/^\#\#/){ print }#header declarations
	else{#true header and variants

		my @col=split(/\t/,$_);
		$col[-1] =~ s/\n$//;

		#die if not two sample columns (11col)
		if(@col != 11){
			die $_."\nERROR: requires exactly two samples in input vcf\n column 10=".$col[9]." (normal), col 11=".$col[10]." (tumor)\n";
		}
	
	
		if(/^\#CHROM/){ 
			print $nad_declare."\n";
			splice(@col,9,1);
		}
		else{#variant line, do work
		
			my @form=split(/:/,$col[8]);
			my @norm=split(/:/,$col[9]);
			my @tum=split(/:/,pop(@col));  


			#add normal's allele depth
			push(@form,$nad);
			push(@tum,$norm[1]);  

			#assign new FORMAT and sample column (tumor)
			$col[8]=join(":",@form);
			$col[9]=join(":",@tum);
		}
		
		print join("\t",@col)."\n";
	}

}
close($vcf_fh);

exit;

