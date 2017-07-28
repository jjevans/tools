#!/usr/bin/env perl
use strict;
use Getopt::Long;

#submit to lsf bwa mem jobs. 
#uses script bwa_mem.pl which must be in path
#input bwa_db R1.fq R2.fq output_sam

#bwa version 0.7+ required.
# must be in path or specified in -e
my $bwa = "bwa";#default in path
my $script = "bwa_mem.pl";

#runtime default values
# canned read group with vals EXP1
my $rg = "'\@RG\\tID:bwa\\tSM:EXP1\\tLB:EXP1\\tPL:illumina'";
my $queue = "pcpgmwgs";
my $bwa = "bwa";#default bwa in path
my $numcore = 1;
my $mem = 12000;

#additional options
GetOptions("s=s"=>\$script,
			"q=s"=>\$queue,
			"t=i"=>\$numcore,
			"m=i"=>\$mem,
			"e=s"=>\$bwa,
			"R=s"=>\$rg);

die "usage: bsub_bwamem.pl -s(cript,path_to_bwa_mem.pl) -q(ueue) -m(emory,bytes) -t(hreads) -e(xecutable to bwa) -R(ead group) bwa_db r1.fq r2.fq output_sam\nRead group, if inputted, must have ID=bwa\n" unless @ARGV == 4;
my $db = $ARGV[0];
my $r1 = $ARGV[1];
my $r2 = $ARGV[2];
my $sam = $ARGV[3];

#bwa_mem.pl -t(hreads) -e(xecutable to bwa) -R(ead group) bwa_db r1.fq r2.fq output_sam
my $bsub = "bsub -q ".$queue." -R 'rusage[mem=".$mem;

if($numcore > 1){
	$bsub .= ",ncpus=".$numcore."] span[hosts=1]' -n ".$numcore;
}
else{
	$bsub .= "]'";
}

$bsub .= " -e aln.err -o aln.out";

my $bwamem_pl=$script." -R ".$rg." -t ".$numcore." -e ".$bwa." ".$db." ".$r1." ".$r2." ".$sam;

my $cmd = $bsub." ".$bwamem_pl;

print "running command: ".$cmd."\n\n";
system($cmd);

exit;



