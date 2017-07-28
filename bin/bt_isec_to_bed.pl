#!/usr/bin/env perl
use strict;

#rearrange first range in bedtools intersect loj 
# and write it in bed format
#reads from stdin and prints to stdout

while(<>){
	my @col = split(/\t/,$_);
	my @bed =splice(@col,0,5);
	

}

exit;
