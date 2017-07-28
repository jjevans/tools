#!/usr/bin/env perl
use strict;

# go through vcf and print all variant lines with coordinate within the intervals from the bed
# filters all variants not in the bed ROIs

die "usage: vcf_filter_bed.pl vcf_file bed_file output_file\n" unless @ARGV == 3;
my $vcf = $ARGV[0];
my $bed = $ARGV[1];
my $out = $ARGV[2];

# go through each variant and iterate through the intervals printing those variants that 
# have a coordinate within one.  Print all vcf header lines.

open(VCF,$vcf) or die "cannot open vcf file\n";
open(BED,$bed) or die "cannot open bed file\n";
open(OUT,">$out") or die "cannot open output file\n";
select(OUT); # have all printing go to OUT handle

while (<VCF>){
	print and next if /^\#/;
	
	my($contig,$location,$rest1) = split(/\t/,$_,3);
	
	foreach my $roi (<BED>){
	
		my($chromo,$start,$end,$rest2) = split(/\t/,$roi,4);	
	
		if($contig eq $chromo and $location >= $start and $location <= $end){
			print;
			last;
		}
	}
	
	seek(BED,0,0);
}

close(VCF);
close(BED);
close(OUT);

exit;
