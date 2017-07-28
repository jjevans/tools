#!/usr/bin/env perl
use strict;

# print stdout a table from genemap2.txt file
# table has omim id (pheno or gene), gene symbol (1st only),description 
# genemap2.txt provides a omim id that is either pheno or gene
# output: id<tab>symbol<tab>description<nl>

die "usage: genemap2_tbl.pl genemap2.txt" unless @ARGV == 1;

open(GM2,$ARGV[0]) or die "cannot open genemap2.txt file.\n";
while(<GM2>){
	my @cols = split(/\|/,$_);
	
	print $cols[8]."\t";
	
	my @syms = split(/ /,$cols[5]);	
	
	print $syms[0]."\t".$cols[7]."\n";
}
close(GM2);

exit;