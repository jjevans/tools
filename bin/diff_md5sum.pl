#!/usr/bin/env perl
use strict;

#get two different files (including dirs) 
# and compare the md5 checksums for them 
#two system calls

die "usage: same_md5sum.pl file1 file2\n" unless @ARGV > 1;

my $cmd = "md5sum ".join(" ",@ARGV);
my $res =`$cmd`;

print "!!YO\n".$res."\nYO!!\n";

exit;

