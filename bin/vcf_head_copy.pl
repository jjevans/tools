#!/usr/bin/env perl
use strict;

#get header from input file 
# and print it to a new file 
# with the filename in 2nd arg

die "usage: vcf_head_copy.pl original_file new_file\n" unless @ARGV == 2;

open(SRC,$ARGV[0]) || die "Cannot open input VCF\n";
open(OUT,">$ARGV[1]") || die "Cannot open output VCF\n";

while(<SRC>){

	if(/^#/){
		print OUT $_;
	}
	else{
		last;
	}
}

close(OUT);
close(SRC);

exit;
