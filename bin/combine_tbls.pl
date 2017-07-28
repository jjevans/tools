#!/usr/bin/perl
use strict;

###
#   uncommon_col.pl
#   JJE, 02.22.2012
#
#   PCPGM
#   Partners Healthcare
###

#takes two tables with common types of ids in first column
#combines all ids from first column of each file making a 
# complete, unique list of ids (all ids concatenated and 
# uniquified)
# combines the rest of the file columns for each file for 
# each id.
# joins all rest of columns in each file by delimiter ":::"
# the delimited contents of first file as argument in column 
# two of output and second file contents in column three
# If an id is in one file, but not another, prints a 
# statement that no contents exist for that id in its 
# respective column.
# this statement is "not_in_file-" + name of file
# !!!Do not have ":::" in filename (or change delim) 
# or it will be hard to parse output of this script.
my $delim = ":::";
my $notinstatement = "not_in_file-";

die "usage: combine_tbls.pl tbl_file1 tbl_file2\n" unless @ARGV == 2;

#hash to keep all contents, each key (id) has an array (2 elements) 
# as value.  first elem is contents of rest of file for file1 and 
# second is for file2
my %contents;

#tbl file 1
open(TBL1,$ARGV[0]) || die "Cannot open table file 1\n";
while(<TBL1>){
	chomp;
	my($id,$rest) = split(/\t/,$_,2);
	
	$rest =~ s/\t/$delim/g;
	
	$contents{$id} = [];#not sure how to make array as value another way
	push($contents{$id},$rest);
	push($contents{$id},$notinstatement.$ARGV[1]);
	
	#print join("\tyo\t",@{$contents{$id}})."\n";
}
close(TBL1);

open(TBL2,$ARGV[1]) || die "Cannot open table file 2\n";
while(<TBL2>){
	chomp;
	my($id,$rest) = split(/\t/,$_,2);
	
	$rest =~ s/\t/$delim/g;
	
	if(!defined($contents{$id})){
		$contents{$id} = [];
		push($contents{$id},$notinstatement.$ARGV[0]);
		push($contents{$id},$rest);
	}
	else{#replace default not in statement
		$contents{$id}[1] = $rest;
	}
}
close(TBL2);

#print 'em all
foreach my $id (keys(%contents)){
	print $id."\t".join("\t",@{$contents{$id}})."\n";
}

exit;
