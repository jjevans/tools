#!/usr/bin/env perl
use strict;
use Getopt::Long;

#bsub any command from stdin
# all arguments expected to be 
# a full command-line when joined 
# and syscalled.
#system run status from shell 
# evaluated and dies if non-zero
my $queue = "pcpgmwgs";
my $mem = 8000;#8Gb
my $numcore;#default 1
my $out = "bsub_cmd.pl.out";
my $err = "bsub_cmd.pl.err";

#additional options
GetOptions("q=s"=>\$queue,
			"n=i"=>\$numcore,
			"m=i"=>\$mem,
			"o=s"=>\$out,
			"e=s"=>\$err);


die "usage: bsub_cmd.pl full_cmdline ex: bsub_cmd.pl ls /tmp\n" unless @ARGV > 0;

#bsub cmd-line
my $cmd = "bsub -q ".$queue." -o ".$out." -e ".$err." -R 'rusage[mem=".$mem;

if(defined($numcore)){
	$cmd .= ",ncpus=".$numcore."] span[hosts=1]' -n ".$numcore;
}
else{
	$cmd .= "]'";
}

#add argument cmd-line
$cmd .= " ".join(" ",@ARGV);

#syscall
die "lsf sumbmission rejected in error command: ".$cmd."\n" if system($cmd);

exit;
