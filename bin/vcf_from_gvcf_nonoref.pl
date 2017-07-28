#!/usr/bin/env perl
use strict;

#convert from gvcf to vcf
#skips all gvcf lines with alt of '.' or '<NON_REF>'
#when valid alt does exist, all multiallelic '<NON_REF>' are removed
#input on stdin, output on stdout
my $non_ref = "<NON_REF>";

while(<>){

	if(/^\#/){
		print;
	}
	else{
		my @arr=split(/\t/,$_);
	
		#skips lines with alt of "." or "<NON_REF>"
		if($arr[4] ne $non_ref && $arr[4] ne '.'){#skip non-variant lines

			#remove all non ref from the valid alts
			s/\,?$non_ref//g;

			print;
		}	
	}

}

exit;

