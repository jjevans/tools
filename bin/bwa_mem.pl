#!/usr/bin/env perl
use strict;
use Getopt::Long;

##run bwa mem with cmd pipe
#input is two paired end fastqs,
# the bwa db, and an output filename.
#bwa must be in path or specify -e

#runtime default values
# canned read group with vals EXP1
my $rg = "\@RG\tID:bwa\tSM:EXP1\tLB:EXP1\tPL:illumina";
my $bwa = "bwa";#default bwa in path
my $numcore = 1;
my $output;#default undef

#additional options
GetOptions("t=i"=>\$numcore,
			"e=s"=>\$bwa,
			"R=s"=>\$rg);

die "usage: bwa_mem.pl -t(hreads) -e(xecutable to bwa) -R(ead group) bwa_db r1.fq r2.fq output_sam\nRead group, if inputted, must have ID of bwa\n" unless @ARGV == 4;
my $db = $ARGV[0];
my $r1 = $ARGV[1];
my $r2 = $ARGV[2];
my $sam = $ARGV[3];

#build cmd
$bwa .= " mem";
$bwa .= " -t ".$numcore;
$bwa .= " -R '".$rg."'";
$bwa .= " ".$db." ".$r1." ".$r2;

#output file
open(SAM,">$sam") || die "Cannot open output sam file: ".$sam."\n";

#run bwa mem
open(CMD,'-|',$bwa) || die "Cannot run bwa with cmd:\n".$bwa."\n";
while(<CMD>){
	print SAM $_;
}
close(CMD);

close(SAM);

exit;
