#!/usr/bin/env perl
use strict;

die "usage: vcf_to_bed.pl vcf_file output_file\n" unless @ARGV == 2;
my $vcffile = $ARGV[0];
my $outfile = $ARGV[1];

open(VCF,$vcffile) || die "cannot open vcf: ".$vcffile."\n";
open(OUT,">$outfile") || die "cannot open vcf: ".$outfile."\n";

while(<VCF>){
	next if /^\#/;
	
	my @col = split;
	
	print OUT $col[0]."\t".$col[1]."\t".($col[1]+1)."\n";
}

close(OUT);
close(VCF);

exit;
