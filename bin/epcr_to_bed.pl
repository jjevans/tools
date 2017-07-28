#!/usr/bin/env perl
use strict;

#e-PCR -m 1750 -t 3 -x + -o oms_f_r.epcr.tbl -v + oms_f_r.sts $HG19

#run NCBI e-PCR and output genomic coordinates 
# for an input set of primers.
#e-PCR must be in your path!
#output is in bed format
#input is same as e-PCR sts file
# 1. file of primer ids and sequences and 
# 2. expected amplicon length (optional, default 1000)
# 3. margin (+/- num bp, optional, default +/-750
# margin of 750 on expected length of 1000 
# allows for amplicon lengths between 250-1750bp
#primer file format (e-PCR sts)
#	primer pair id
#	forward primer sequence
#	reverse primer sequence
#	expected amplicon length
my $expect_len = 1000;#defaults
my $margin = 750;
my $bedscore = 0;#arbitrary value for unused bed format score

die "usage: epcr_to_bed.pl primer_file genome_file expected_amplicon_length(optional, default 1000) margin(+/-,optional,default 750)\n" if @ARGV < 2;

#set user inputted expected files and length and margin 
my $primer_file = $ARGV[0];
my $genome_file = $ARGV[1];
$expect_len = $ARGV[2] if defined($ARGV[2]);
$margin = $ARGV[3] if defined($ARGV[3]);

#die if length range messed
die "Expect length: ".$expect_len." less than or equal to the margin: ".$margin."\n" if ($expect_len-$margin) <= 0;

#epcr
my $cmd = "e-PCR";
$cmd .= " -t 3";#epcr output 3

#amplicon length range
my $range = [$expect_len - $margin,$expect_len + $margin];
$cmd .= " -d".join("-",@$range);
#shout amplicon length range
#print STDERR "amplicon length range: (".join(",",@$range).")\n";

#input and gen ref file
$cmd .= " ".$primer_file;
$cmd .= " ".$genome_file;
print STDERR "epcr cmd: ".$cmd."\n";

#cmd pipe
open(CMD,'-|',$cmd) || die "Cannot open command pipe for command: ".$cmd."\n";
while(<CMD>){
	chomp;
	my @col = split(/\t/,$_);

	#bed format
	print $col[0]."\t".$col[3]."\t".$col[4]."\t".$col[1]."\t".$bedscore."\t".$col[2]."\n";
}
close(CMD);

exit;

