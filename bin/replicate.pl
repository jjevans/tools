#!/usr/bin/env perl
use strict;

#make many files from one modifying by inputted regex
#input is file, regex to append file number to, num files

die "usage: replicate.pl file regex_from regex_to num_files\n" unless @ARGV == 3;

my $file0 = $ARGV[0];
my $pattern = $ARGV[1];
my $num = $ARGV[2];

chomp($file0);
open(my $f0,$file0) || die "cannot open: ".$file0."\n";

for(my $i=0;$i<$num;$i++){
	my $file1 = $file0."_".$i;
	open(my $f1,">$file1") || die "cannot open new file: ".$file1."\n";
	foreach my $line (<$f0>){
		$line =~ s/$pattern/$pattern$i/g;
		print $f1 $line;
	}

	seek($f0,0,0);
	close($f1);
}
close($f0);

exit;

