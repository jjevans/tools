#!/usr/bin/env perl
use strict;

#!!!UNFINISHED!!!
#from a sequence file and range of coordinates 
# (fasta id, start-end), pull out the sequence 
# falling into that location
#dies if range out of bounds (seq shorter 
# than requested range).
#range is a set of start and end nt locations 
# separated by "-"
#fasta id is whatever that sequence is 
# named in the file.  A genome fasta would 
# have a chromosome number

die "usage: substr_fa.pl fasta_file fasta_id range(ex. 1000-2569)\n" unless @ARGV == 3;
my $seqfile = $ARGV[0];
my $chr = $ARGV[1];
my($start,$end)=split(/-/,$ARGV[2]);

open(SEQ,$seqfile) || die "Cannot open sequence fasta file\n";

$/="\n>";
while(<SEQ>){
	print "here".$_."there\n\n\n"
}
close(SEQ);

exit;
