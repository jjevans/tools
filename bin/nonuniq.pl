#!/usr/bin/env perl
use strict;

#print any line that have duplicate in the input file
# only prints one line found to be duplicate

die "usage: notuniq.pl tbl_file\n" unless @ARGV == 1;

my %ids;

open(FILE,$ARGV[0]) || die "Cannot open file.\n";
while(<FILE>){
	chomp;
	$ids{$_}++;
}
close(FILE);

#print dups
foreach my $item (sort(keys(%ids))){
	print $item."\n" if $ids{$item} > 1;
}

exit;
