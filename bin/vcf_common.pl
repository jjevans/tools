#!/usr/bin/env perl
use strict;

# outputs the variants common to both files.  prints header from first file.
# prints lines from the first vcf

die "usage: common_variant.pl vcf1 vcf2\n" unless @ARGV == 2;
my $vcf1 = $ARGV[0];
my $vcf2 = $ARGV[1];

open(VCF1,$vcf1) or die "cannot open first vcf\n";
open(VCF2,$vcf2) or die "cannot open second vcf\n";

while(<VCF1>){
	print and next if /^\#/;
	
	my($contig1,$position1,$rest1) = split(/\t/,$_,3);
	
	foreach my $mutation (<VCF2>){
		next if $mutation =~ /^\#\#/;
		
		my($contig2,$position2,$rest2) = split(/\t/,$mutation,3);
		
		if($contig1 eq $contig2 and $position1 == $position2){
			print;
			last;
		}
	}
	
	seek(VCF2,0,0);
}

close(VCF1);
close(VCF2);

exit;
