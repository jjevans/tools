#!/usr/bin/env perl
use strict;

#compare md5sum checksums between 
# all files input and print out 
# the files with the same checksums

die "usage: same_md5sum.pl file1 file2\n" unless @ARGV > 1;

my $cmd = "md5sum ".join(" ",@ARGV);
my $res =`$cmd`;

my @sums = split(/\n/,$res);

print $res."\n:::\n";
exit;

