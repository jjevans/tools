#!/usr/bin/env perl
use strict;

#remove normal sample column in mutect output vcf 
#decision made if header sample name has a "T" for tumor
#makes normal sample first col then the tumor sample has 
# the following column
#output to stdout
#example ids for tumor and normal used from header name of vcf sample
#	SSEQ_M18PT_gDNA SSEQ_M18XN_gDNA

#input is file with mutect output vcf format
die "vcf_mutect_ordr.pl vcf_mutect_output\n" unless @ARGV == 1;
my $vcf = $ARGV[0];

my $do_reordr = 0;#no reorder necessary (0)

open(my $vcf_fh,$vcf) || die "Cannot open input vcf file\n";
while(<$vcf_fh>){

	if(/^\#\#/){print}
	else{
		my @col=split(/\t/,$_);
		$col[-1]=~s/\n$//; 

		if(/^\#CHROM/){ 
			my @huh=split(/_/,$col[9]); 
			
			if($huh[1]=~/T/){
				$do_reordr = 1;
			} 
		}

		if($do_reordr){
			my $norm = pop(@col);
			splice(@col,-1,0,$norm);
		}

		print join("\t",@col)."\n";
	}
}
close($vcf_fh);

exit;

