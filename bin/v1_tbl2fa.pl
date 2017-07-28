#!/usr/bin/env perl
use strict;

#take a table of id<tab>sequence<nl> and 
# output fasta file with length of seq in description
#input on stdin from fa2tbl.pl (fasta2tbl.pl)
#ex. cat file.fa | fa2tbl.pl | tbl_seq_len.pl
#add any arg to cmd-line and prints length
my $print_desc = 1;
$print_desc = 0 if defined($ARGV[0]);


while(<STDIN>){

	my($id,$seq) = split(/\t/,$_);
	$seq =~ s/\n$//;
	
	my $len = length($seq);

	#format seq to 60chars/line
	$seq =~ s/(.{60})/\1\n/g;

	my @parts = split(/\|\|/,$id);	

	print shift(@parts);#id w/o desc

	
	if(@parts && $print_desc){
		print "\t".join(" ",@parts);
	}
	
	print "\n".$seq."\n";
}

exit;

