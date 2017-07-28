#!/usr/bin/env perl
use strict;

my $print_only = 0;#default execute sys call

die "usage: mkdir_and_cd.pl directory only_print_cmd(optional,0=syscall)\n" unless @ARGV > 0;
my $dir = $ARGV[0];
$print_only = $ARGV[1] if defined($ARGV[1]);

my $cmd = "mkdir ".$dir." \x26\x26 cd ".$dir;

print "SYSTEM: ".$cmd."\n";
system($cmd) unless $print_only;

exit;
