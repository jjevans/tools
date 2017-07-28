#!/usr/bin/env perl
use strict;

#convert fasta to table
#description in fasta not in output
#removes ">"
my $delim = "||";
my $print_desc = 0;
$print_desc = 1 if defined($ARGV[0]);#if argv0, then print desc

my $nl = 0;#no newline first row
while(<STDIN>){
	chomp;
		
	#ex >id desc	
	if(/^>(.+?)\s*(.*?)\s*$/){
		
		#pull out id exclusively
		my $id = $1;
		
		my $desc = $2;

		if($print_desc && $desc ne ""){#delim desc to id

			#format, delimit to id
			$desc =~ s/^\s+//;
			$desc =~ s/\s+$//;
			$desc =~ s/\s+/$delim/g;
			
			$id .= $delim.$desc;
		}

		#prints newline prior to output line except 1st line
		if(!$nl){#skip 1st seq
			$nl++;#non-zero
		}
		else{
			print "\n";
		}
		
		print $id."\t";
	}
	else{
		#s/\s+$//;
		print;
	}
}

print "\n";

exit;

