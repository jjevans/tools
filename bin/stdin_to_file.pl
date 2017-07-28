#!/usr/bin/env perl
use strict;

#print stdin to a file
#input is whatever on stdin 
#and an argument of a file to 
# write to

die "usage: echo blahblah | stdin_to_file.pl filename\n" unless @ARGV == 1;
die "no input from stdin.\n" if -t STDIN;

open(OUT,">$ARGV[0]") || die "cannot open file: ".$ARGV[0]."\n";
while(<STDIN>){
	print OUT $_;
}
close(OUT);

exit;
