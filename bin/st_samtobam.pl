#!/usr/bin/env perl
use strict;

#samtools syscall sam to bam conversion
# samtools view -bS -o file1.bam file1.sam

die "usage: st_samtobam.pl input_sam_filename output_bam_filename\n" unless @ARGV == 2;
my $insam = $ARGV[0];
my $outbam = $ARGV[1];

my $cmd = "samtools view -bS -o ".$outbam." ".$insam;
my $status = system($cmd);
print $status."\tyo\n";

exit;
