#!/usr/bin/env perl
use strict;

#convert fasta to table
#description in fasta not in output
#removes ">"
my $delim = "||";
my $print_desc = 0;
$print_desc = 1 if defined($ARGV[0]);


my $print_nl = 0;
while(<>){
	s/\n$//;

	if(s/^>//){

		#prints newline prior to output line except 1st line
		if(!$print_nl){#skip 1st seq
			$print_nl++;#non-zero
		}
		else{
			print "\n";
		}

		s/^>(.+?)\s(.*)$/\1/;#pull out id exclusively
		$_ .= $delim.$2 if defined($2) && $print_desc;

		print $_."\t";
	}
	else{
		print;	
	}
}

print "\n";

exit;

