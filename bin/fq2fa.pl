#!/usr/bin/env perl
use strict;

#jje 09/2021
#convert fastq to fasta format sequence files

my $id_cnt = 4;
my $seq_cnt = 3;

while(<>){
	if($id_cnt%4==0){
		chomp;
		my @flds = split(/ /, $_);
		print ">".$flds[0]."\n";
		$id_cnt = 1;
	}
	else{
		$id_cnt++;
	}

	if($seq_cnt%4==0){
		print;
		$seq_cnt = 1;
	}
	else{
		$seq_cnt++;
	}	
}


