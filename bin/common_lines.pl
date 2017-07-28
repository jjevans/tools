#!/usr/bin/env perl
use strict;

# print all lines common to 2 text files.
# Use uniquely sorted input files so 
# no duplicate lines in either file

die "usage: common_lines.pl tblfile1 tblfile2\n" unless @ARGV == 2;

open(F1,$ARGV[0]) || die "cannot open first file.\n";
open(F2,$ARGV[1]) || die "cannot open second file\n";

my %lines1;
while(<F1>){
	$lines1{$_}++;
}

while(<F2>){
	print if exists($lines1{$_});
}

close(F1);
close(F2);

exit;
