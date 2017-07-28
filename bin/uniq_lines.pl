#!/usr/bin/env perl
use strict;

# don't print the lines that have had the same id printed before
# (skips lines with duplicate ids).

die "usage: uniq_lines.pl table_file\n" unless @ARGV == 1;

my %used;

open(TBL,$ARGV[0]) || die "Cannot open file.\n";
while(<TBL>){
	
	chomp;#in case only one column

	my($id,$rest)=split(/\t/,$_,2);

	print $_."\n" unless defined($used{$id});
	
	$used{$id}++;#placeholder, value unused
}
close(TBL);

exit;
