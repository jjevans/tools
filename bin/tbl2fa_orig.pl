#!/usr/bin/env perl
use strict;

#convert a table with id<tab>sequence<newline> 
# to a fasta file
#print sequence in 60bp lines
#default delim to parse description is "||" 
# but argv0 will override
my $delim = "||";
my $print_desc = 1;#print any delimited desc by default
$print_desc = 0 if defined($ARGV[0]);#if description in id w/ delim

my $print_len = 1;
$print_len = 0 if defined($ARGV[1]);

while(<STDIN>){
	my($id,$seq)=split;
	
	my @parts = split(/\|\|/,$id);
	$id = shift(@parts);
	
	$id .= "\t".join(" ",@parts) if @parts && $print_desc;
	
	$seq =~ s/(.{60})/\1\n/g;
	
	#remove trailing nl if exactly 60char
	$seq =~ s/\n$//;

	print ">".$id."\n".$seq."\n";
}

exit;
