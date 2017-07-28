#!/usr/bin/env perl
use strict;
use Getopt::Long;
use bt_util;

#average coverage over intervals from 
# a bamfile
#runs bedtools coverage using split, 
# chunks by sliding window, 
#outputs bed file of avg coverage by windows 
#input is a bamfile, 
# intervals (roi, bed,optional,
#	default all contiguous line by pos),
# length of window (optional, default 100bp),
# overlap of each window (optional, 
#	default 1/2 length of window)

#bam file required
my $bam;
my $bed;#target intervals
my $index;#run tabix
my $out_fh = *STDOUT;

my $len = 100;#win len
my $overlap = $len * 0.5;#win overlap

my %bt_arg = ();
#run vals
my %bt_arg = (\$bam,
			 "l"=>\$len,
			 "ol"=>\$overlap,
			 "bgz"=>\$index,
			 "f"=>\$output);
GetOptions(\%bt_arg,"l=i","ol=i","bgz","f=s");

die "usage: bt_cov_win.pl -l(ength of window) -ol (overlap of windows) -f (output file) align.bam\n\
		required: bam formatted alignment file\n\
		optional:\n\
			-l length of window (100bp)\n\
			-ol amount overlap of adjacent windows (1/2 length of window)\n\
			-f output file (stdout)\n\
			-bgz index inputted bamfile (true)\n\
		use -bgz unless a tabix index exists for the alignments\n" unless @ARGV == 1;
$bt_arg{"bam"} = $ARGV[1];

my $bt_obj = bt_util->new(\%bt_arg);



exit;
	