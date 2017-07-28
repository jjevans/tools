#!/usr/bin/env perl
use strict;

#___!!!UNFINISHED!!!

#from a vcf file print all 
# variants having the same 
# position in a bedfile having 
# each position with the same 
# chromosome start and end.
# ex. chr1	251	251
#NOTE: prints the whole vcf 
# header if third argument 
# provided (can be anything)

die "usage vcf_by_pos.pl vcf_file.vcf single_position.bed print_vcf_header(non-zero, optional)\n" unless @ARGV >= 2;

my %pos;

open(POS,$ARGV[1]) || die "Cannot open single position bed file.\n";
while(<POS>){
		my @col = split;
		
		$pos{$col[0]:$col[1]} = 1;#unused value
}
close(POS);

open(VCF,$ARGV[0]) || die "Cannot open vcf file\n";
while(<VCF>){
	if(/^\#/){
		print if defined($ARGV[2]);
	}
	else{
		my($chr,$loc,$rest) = split(/\t/,$_,3);
		print $chr.":::".$loc."-----".$rest;

		print if exists($pos{$chr.":".$loc});
	}
}
close(VCF);

exit;
