#!/usr/bin/env perl
use strict;

#convert all multiallelic variants (multiple alts, wide form) 
# to one variant per line (one alt, multiple lines of same pos, tall form)
#jje16, msl34, personalized medicine, biofx 05152015

#input on stdin, output on stdout

#usage if no stdin
if(-t STDIN){
	die "usage: vcf_wide_to_tall.pl (input vcf on stdin)\n"; 
}


while(<STDIN>){
	if(/^#/){
		print;
	}
	else{
		my @col = split(/\t/,$_);
	
		my @alts = split(/\,/,$col[4]);
	
		foreach my $alt (@alts){
			my @col_cp = @col;
		
			$col_cp[4] = $alt;
			print join("\t",@col_cp);
		}
	}
	
}

exit;

