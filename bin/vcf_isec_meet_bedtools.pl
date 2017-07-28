#!/usr/bin/env perl
use strict;

#vcf intersect meets bedtools
#prints the vcf lines of vcf1 that have the 
# same variant position as those of vcf2.
#vcf2 may be a vcf or bedfile though only 
# looks at first coord in bedfile.
#vcf1 should be the larger vcf as vcf2's 
# positions are read into memory.
#does not print vcf header

die "usage: vcf_isec_meet_bedtools.pl vcf1 vcf2 print_vcf2(any value,optional,default print vcf1)\n" unless @ARGV > 1;

my %loc;
open(VCF2,$ARGV[1]) || die "Cannot open second vcf file.\n";
while(<VCF2>){
	next if /^\#/;
	
	my($chr,$pos,$rest) = split(/\t/,$_,3);
	$loc{$chr.":".$pos} = $_;
}
close(VCF2);

open(VCF1,$ARGV[0]) || die "Cannot open first vcf file.\n";
while(<VCF1>){
	next if /^\#/;

	my($chr,$pos,$rest) = split(/\t/,$_,3);
	my $loc_key = $chr.":".$pos;
	
	if(exists($loc{$loc_key})){
	
		if(defined($ARGV[2])){#print vcf2
			print $loc{$loc_key};
		}
		else{#print vcf1
			print;
		}
	}
}
close(VCF1);

exit;