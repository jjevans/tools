#!/usr/bin/env perl
use strict;

# get frequency of the number of times 
# a column is different between a file 
# of merged tables (output of merge_tbls.pl).
# The output of merge_tbls.pl is a table file 
# with each value being a combination of value1 
# concatenated by ":::" to value2.  value1 
# derives from the value found in the first 
# table that was merged and value2 is the value 
# found in the second table.
# This script keeps track of the columns (by 
# column name found in 1st line header.  
# It goes through each line and increments 
# a counter for that column if value1 is 
# different from value2.
# It outputs a 2 column table with 1st 
# column of the header column name and 
# the second column the frequency of 
# values different from each other.
# Ignores first column which is a unique 
# id and isn't to be compared (not delimited).
# Compares by a string equals (not ever numerical).
# Unique column names required so only reported once.
my $delim = ":::";

die "usage: tally_merged.pl merged_table_file (from merge_tbls.pl)\n" unless @ARGV == 1;

open(MERGED,$ARGV[0]) || die "cannot open merged table file\n";
my @lines = <MERGED>;
close(MERGED);


#column names
my $headline = shift(@lines);
chomp($headline);
my @colnames = split(/\t/,$headline);

#initialize tallies to 0
my %tallies;
for(my $i=1;$i<@colnames;$i++){
	$tallies{$colnames[$i]} = 0;
}


#tally columns
foreach my $line (@lines){
	chomp($line);
	my @cols = split(/\t/,$line);
	
	#starts with 1 because skips unique id in column 1
	for(my $i=1;$i<@cols;$i++){
		my($val1,$val2) = split(/$delim/,$cols[$i]);
		
		if($val1 ne $val2){
			$tallies{$colnames[$i]}++;
		}
		
	}
}


#print tallies by column name
foreach my $key (keys(%tallies)){
	print $key."\t".$tallies{$key}."\n";
}

exit;
