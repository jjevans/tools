#!/usr/bin/env perl
use strict;

#stdin input e-pcr file and output to stdout a bedfile
# bed score value = 0

while(<>){

	chomp;
	my @col = split(/\t/,$_);

	#bed format
	print $col[0]."\t".$col[3]."\t".$col[4]."\t".$col[1]."\t0\t".$col[2]."\n";
}

exit;
