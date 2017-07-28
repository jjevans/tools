#!/usr/bin/env perl
use strict;

#pull all lines from file2 that exist in file1
#efficient mem with file2 so file2 should be the 
#memory hog (db)
my $del = 0;#default do not print unmatched ids to stderr

die "usage: common_pull.pl file1(file (lst,tbl) with ids to pull) file2(to pull lines from) print_stderr_variant_with_no_match(optional,0/1,false)\n" unless @ARGV > 1;
my $file1 = $ARGV[0];
my $file2 = $ARGV[1];
$del = $ARGV[2] if defined($ARGV[2]);

#file1
my %f1;
open(my $f1_fh,$file1) || die "Cannot open first file: ".$file1."\n";
while(<$f1_fh>){
	s/\n$//;
	my @col = split(/\t/,$_);
	
	$f1{$col[0]} = $_;
}
close($f1_fh);

#file2
open(my $f2_fh,$file2) || die "Cannot open second file: ".$file2."\n";
while(<$f2_fh>){
	my @col = split(/\t/,$_);

	if(exists($f1{$col[0]})){
		print;

		#delete from hash one in case want to know 
		# what didn't have an entry in file2
		delete($f1{$col[0]}) if $del;
	}
}
close($f2_fh);

if($del){
	foreach my $nomatch(keys(%f1)){
		print STDERR $nomatch."\n";
	}
}
exit;
