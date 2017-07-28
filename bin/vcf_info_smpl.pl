#!/usr/bin/env perl
use strict;

#take info column and put it in the sample's 
# column.
# 1st arg is to vcf to format 
# 2nd arg is output filename
# 3rd arg makes INFO append to 
#  existing sample info (none replaces it).
my $smpl_col = 9;#10th column, change if another sample desired
my $delim = ":";

die "usage: vcf_info_smpl.pl in_vcf out_vcf append_info_to_existing_sample info(optional,any value)\n" unless @ARGV > 1;
my $invcf = $ARGV[0];
my $outvcf = $ARGV[1];
my $append = $ARGV[2];#undef if replace

open(VCF,$invcf) || die "Cannot open input vcf: ".$invcf."\n";
open(OUT,">$outvcf") || die "Cannot open output vcf: ".$outvcf."\n";
#select(OUT);

while(<VCF>){

	if(/^\#/){print OUT $_;}
	else{
		chomp;
		
		my @col = split(/\t/,$_);
		
		warn "No sample column in this row\n" if @col <= 9;
		
		if(defined($append)){
			my $smpl = $col[$smpl_col];
			$col[$smpl_col] = $col[7].$delim.$smpl;
		}
		else{
			$col[$smpl_col] = $col[7];
		}
		
		print OUT join("\t",@col)."\n";
	}	
}
close(OUT);
close(VCF);

exit;
