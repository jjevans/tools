#!/usr/bin/env perl
use strict;

# sample of file for the inputted number of lines

die "pull out a sample of lines from a file.\noptional third argument to skip all lines starting with pound sign (don't supply anything if to include).\nusage: sampler.pl file num_samples skip_pound(optional)\n" if @ARGV < 2;
open(FILE,$ARGV[0]) || die "cannot open file\n";
my $sample_num = $ARGV[1];
my $skip = $ARGV[2];#skip pound signs

my @lines;
while(<FILE>){
	next if (/^\#/ and defined($skip));
	push(@lines,$_);
}

if(@lines < $sample_num){
	die "not enough lines (".@lines.") in file for the sample number provided!\nremember valid lines do not start with pound sign if 3rd argument provided.\n";
}

for(my $i=0;$i<$sample_num;$i++){
	my $line_num = int(rand(@lines));

	print splice(@lines,$line_num,1);
}

exit;