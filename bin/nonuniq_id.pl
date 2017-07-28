#!/usr/bin/env perl
use strict;

# print the lines from a file 
# that have duplicate ids in first column
# prints all non unique ids so there will 
# be duplicates in the output to this script.

die "usage: not_uniq_id.pl tbl_file\n" unless @ARGV == 1;


my %entries;
my %numtimes;

open(FILE,$ARGV[0]) || die "Cannot open file.\n";
while(<FILE>){
	chomp;
	my @cols = split(/\t/,$_);
	$entries{$cols[0]} = $_;
	$numtimes{$cols[0]}++;
}
close(FILE);

#print dups
foreach my $id (sort(keys(%entries))){
	print $entries{$id}."\n" if $numtimes{$id} > 1;
}

exit;
