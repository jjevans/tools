#!/usr/bin/env perl
use strict;

# outputs the variants uncommon to both files.  prints those snps from 1st vcf not in 
# the 2nd vcf.  prints header from first file.

die "usage: uncommon_variant.pl vcf1 vcf2\n" unless @ARGV == 2;
my $vcf1 = $ARGV[0];
my $vcf2 = $ARGV[1];

# load 2nd vcf into hash with contig:::position as key and whole line as value
my %variants;
open(VCF2,$vcf2) or die "cannot open first vcf\n";
while(<VCF2>){
	next if /^\#/;
	
	my($contig,$position,$rest) = split(/\t/,$_,3);
	
	$variants{$contig.":::".$position}++; # keep track of how many times a variant exists
}
close(VCF2);

# print all variants that don't have an existing contig and position in the hash
open(VCF1,$vcf1) or die "cannot open second vcf\n";
while(<VCF1>){
	print and next if /^\#/;
	
	my($contig,$position,$rest) = split(/\t/,$_,3);
	
	print unless exists($variants{$contig.":::".$position});
}
close(VCF1);

exit;
