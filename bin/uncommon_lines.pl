#!/usr/bin/env perl
use strict;

# print all lines not common to 2 text files.
# only prints file1's lines that don't exist 
# in file2.
# Use uniquely sorted input files so 
# no duplicate lines in either file

die "usage: uncommon_lines.pl tblfile1 tblfile2\n" unless @ARGV == 2;

open(F1,$ARGV[0]) || die "cannot open first file.\n";
open(F2,$ARGV[1]) || die "cannot open second file\n";

my %lines2;
while(<F2>){
	$lines2{$_}++;
}

while(<F1>){
	if(!exists($lines2{$_})){
		print;
	}
}

close(F1);
close(F2);

exit;
