#!/usr/bin/env perl
use strict;

#print any line that have duplicate in the input file
# only prints one line found to be duplicate
#prints whole line regardless of whitespace with 
# the last col being the number of times the dup 
# line was encountereed

die "usage: notuniq_cnt.pl tbl_file\n" unless @ARGV == 1;

my %ids;

open(FILE,$ARGV[0]) || die "Cannot open file.\n";
while(<FILE>){
	chomp;
	$ids{$_}++;
}
close(FILE);

#print num dups
foreach my $item (sort(keys(%ids))){
	print "\"".$item."\"\t".$ids{$item}."\n" if $ids{$item} > 1;
}

exit;
