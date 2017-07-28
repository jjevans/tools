#!/usr/bin/env perl
use strict;

#!!!___UNFINISHED___!!!
#run bedtools intersect on a bam 
# to find overlapping alignments 
# to a bedfile

#input is a bamfile, a bedfile 
# and a file to output it to
die "usage: bt_isec_aln.pl alignments.bam intervals.bed output_filename\n" unless @ARGV > 1;
my $bam = $ARGV[0];
my $bed = $ARGV[1];
my $outfile = $ARGV[2];

my $out;
if(defined($outfile)){
	open($out,">$outfile") || die "cannot open file: ".$outfile."\n";
}
else{
	$out = *STDOUT;
}

#my $cmd = "bedtools intersect -wao -bed -nobuf -abam ".$bam." -b ".$bed;
my $cmd = "bedtools intersect -bed -nobuf -abam ".$bam." -b ".$bed;

my %loc;
open(my $pipe,'-|',$cmd) || die "Can't run bedtools intersect.\nCMD: ".$cmd."\n";
while(<$pipe>){
	s/\n$//;
	my @col = split(/\t/,$_,7);
	pop(@col);#get rid of col 7-12
	
	my($id,$end) = split(/\//,$col[3]);
	
	my $pos = join(":",splice(@col,0,3));

	if(!exists($loc{$pos})){#init
	
		#array of arrays
		# arr1=read id, arr[2]=mapping quality, 
		# arr3=strand, arr4=pair end number (1/2)
		$loc{$pos} = { "coverage" => 0, "read" => [[],[],[],[]] };
	}
	
	push(@{$loc{$pos}{"read"}[0]},$id);
	push(@{$loc{$pos}{"read"}[1]},$col[4]);
	push(@{$loc{$pos}{"read"}[2]},$col[5]);
	push(@{$loc{$pos}{"read"}[3]},$end);
	$loc{$pos}{"coverage"}++;
}
close(CMD);


exit;
