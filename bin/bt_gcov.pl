#!/usr/bin/env perl
use strict;
use Getopt::Long;


#parse bedtools genomecov output 
# to use to calculate coverage 
# over intervals

# required is either of
# 1. input is a bam (-bam), bedfile (-bed), and 
# at least one coverage cutoff (-bin) to split 
# into bins.  more bins is more useful
# 2. input a file of genomecov output (opt -norun)
# required=bam,bed or genomecov.out

#prints stdout unless -out option specified with filename
my $usage = "usage:\tbt_gcov.pl -bam file.bam -bed file.bed\n\tbt_gcov.pl -norun file.tbl\n\tbt_gcov.pl -norun file.tbl -bin 10 -bin 25 -bin 62\n\
	Required: a target bed file (-bed) and either a bam file (-bam) \n\t or a file of existing bedtools genomecov output (-norun).\n\tOptional: thresholds for bins (default=5,15,30,60,90,120)\n";

#defaults
my $out_fh = *STDOUT;
my @default_bins = (5,15,30,60,90,120);

my $bins = [];
my %opt = ("bam" => undef, "bed" => undef, "norun" => undef, "bin" => $bins, "out" => undef);

GetOptions(\%opt,"bam:s","bed:s","norun:s","bin:i@","out:s");

##intervals
die $usage."\n\ntarget bedfile required.\n" unless defined($opt{"bed"});

#init arrays by chromosome
my %intrvl;
open(BED,$opt{"bed"}) || die "ERROR: unable to open bedfile: ".$opt{"bed"});
while(<BED>){
	s/\n$//;
	my($chr,$start,$stop,$rest) = split(/\t/,$_,3);
	my $pos = $chr.":".$start.":".$stop;
	my $len = $stop-$start;

	#init
	unless(exists($intrvl{$pos}){
		$intrvl{$pos} = [];
		$intrvl{$pos}[0..$len-1] = (0) x $len;
	}
}
close(BED);


#find if run bedtools or just use a file
my $run_it = cmd_or_file(\%opt);

#assign bins of default unless user input
$bins = \@default_bins unless @{$bins};



my $in_fh;
if(!defined($$run_it)){
	die $usage."\n\nneeds either a bamfile (-bam) to run genomecov with\n or a results file (-norun) to process.\n";
}
elsif($$run_it){
	die "TEMPORARY ERROR: can't run it!\n";
	print "yo\n";
	my $cmd;
	open($in_fh,$cmd) || die "ERROR: cannot run command: ".$cmd."\n";
}
else{
	open($in_fh,$opt{"norun"}) || die "ERROR: cannot open genomecov output file: ".$opt{"norun"}."\n";
}

#process
while(<$in_fh>){
	s/\n$//;
	my($chr,$start,$stop,$cov) = split(/\t/,$_);

	increment();
}
close($in_fh) unless $$run_it;

#assign new file to direct output
open($out_fh,">".$opt{"out"}) || die "cannot open output file: ".$opt{"out"}."\n" if defined($opt{"out"});
close($out_fh) if defined($opt{"out"});


exit;


sub cmd_or_file{
	#check hash for defined 
	# value in keys "bam" and "bed"
	my $info = $_[0];

	my $retval;
	if(defined($info->{"bam"})  && -B $info->{"bam"}){
		$retval = 1;
	}
	elsif(defined($info->{"norun"}) && -T $info->{"norun"}){
		$retval = 0;
	}
	
	return \$retval;
}

sub increment{
	#increment each position in an array 
	# based on a start and stop position 
	# (maybe map?)
	my $arr = $_[0];
	my $i = $_[1];
	my $j = $_[2];
	
	return;
}

	
	
}