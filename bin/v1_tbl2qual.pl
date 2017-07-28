#!/usr/bin/env perl
use strict;

#convert a table with id<tab>sequence<newline> 
# to a fasta file
#print sequence in 60bp lines

while(<>){
	s/\n$//;
	my($id,$seq)=split(/\t/,$_);
	
	$seq =~ s/(.{60})/\1\n/g;
	
	#remove trailing nl if exactly 60char
	$seq =~ s/\n$//;

	print ">".$id."\n".$seq."\n";
}

exit;
