#!/usr/bin/env perl
use strict;

#convert fasta to table
#description in fasta not in output
#removes ">"
my $delim = "--";
my $print_desc = 0;
$print_desc = 1 if defined($ARGV[0]);#if argv0, then print desc

my $nl = 0;#no newline first row
while(<STDIN>){
	s/\n$//;
		
	#ex >id desc	
	if(s/^>//){
		my @parts = split(/\s+/,$_);
		
		#pull out id, any description
		my $id = shift(@parts);

		my $desc;
		if($print_desc && @parts > 0){#delim desc to id

			#delimit to id
			$desc = join($delim,@parts);			
			#$desc =~ s/\s+/$delim/g;
			
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
		print;
	}
}

print "\n";

exit;

