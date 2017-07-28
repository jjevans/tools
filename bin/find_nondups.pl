#!/usr/bin/env perl
use strict;

# from a table having duplicate lines, get the lines with the 
# same 1st column (id), but with different info in the rest of 
# the columns. 
# essentially, it prints any ids that don't sort unique
#
# ex.
#	id1	data1
#	id2	data2
#	id3	data3
#	id1 data4
#
# would give the id id1 since line 1 has id1 with data1 and in 
# row 4 id1 has different data data4.
#
# Input is from stdin and prints to stdout
# delimiter is tab

my %info;
while(<>){
	my($id,$rest)=split(/\t/,$_,2);
	
	if(!defined($info{$id})){
		$info{$id}=$rest;
	}
	else{
		if($rest ne $info{$id}){
			chomp($info{$id});print $id."\t".$info{$id}."\t".$rest;
			
		}
	}
}

exit;
