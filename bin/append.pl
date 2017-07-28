#!/usr/bin/env perl
use strict;

die "usage: append.pl filetoappendto filetoappend\n" unless @ARGV == 2;

open(FIN,">>$ARGV[0]") || die;
open(CON,$ARGV[1]) || die;
while(<CON>){print FIN $_;}
close(FIN);
close(CON);

exit;

