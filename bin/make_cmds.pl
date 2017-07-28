#!/usr/bin/env perl
use strict;

#make bsub cmds of bwa mem for all inputted file pairs

#output file is the R1 filename with ".sam" suffix appended

#bwa version 0.7 required which in hs747 home
my $bwaexec = "/scratch/pcpgm/hs747/softwares/bwa-0.7.9a/bwa";
die "bwa executable hard coded and nonexistent!!! ".$bwaexec."\n" unless -f $bwaexec;

#defaults
my $numproc = 8;
my $mem = 36000;
my $rg = "'\@RG\\tID:AS\\tSM:AS\\tLB:AS\\tPL:illumina'";

die "usage: make_cmds.pl bwa_db_base_file R1_file R2_file\n" unless @ARGV==3;
my $db = $ARGV[0];
my $r1 = $ARGV[1];
my $r2 = $ARGV[2];

#make output filename
my $sam = $r1.".sam";

my $bsub = "bsub -q pcpgmwgs -n ".$numproc." -R 'rusage[mem=".$mem.",ncpus=".$numproc."] span[hosts=1]' -e aln.err -o aln.out";
my $bwa=$bwaexec." mem -R ".$rg." -t ".$numproc." ".$ARGV[0]." ".$ARGV[1]." ".$ARGV[2]." > ".$sam;

my $cmd = $bsub." ".$bwa;

print $cmd."\n";
exit;



