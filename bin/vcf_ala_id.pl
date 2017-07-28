#!/usr/bin/env perl
use strict;

#make a unique id out of pos and change to 
# use in wgs anno to produce the alamut vcf 
# for the uploader
#jje16, msl34, personalized medicine 05152015

#input on stdin, output on stdout
#also makes it 10 col to avoid alamut error
#fills in empty added cols with '.'

#usage if no stdin
if(-t STDIN){
	die "vcf_ala_id.pl (input vcf on stdin)\n";
}


while(<STDIN>){
	
	if(/^\#/){
		print;
	}
	else{
		my @col = split(/\t/,$_);
		
		my $id = $col[0].":".$col[1].$col[3].">".$col[4];
		
		$col[2] = $id;
		
		print join("\t",@col);
	}
}

exit;
