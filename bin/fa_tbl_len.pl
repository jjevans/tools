#!/usr/bin/env perl
use strict;

#print length of second col of table on stdin

while(<>){
	chomp;
	my($id,$seq) = split(/\t/,$_);
		
	print $id."\t";
	
	#handle phred quals
	my @bp = split(/ /,$seq);

	if(@bp == 1){#normal seq
		print length($seq);
	}
	else{#phred qual
		print scalar @bp;
	}
	
	print "\n";

}

exit;
