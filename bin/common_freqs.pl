#!/usr/bin/env perl
use strict;

# take a 2 column table from stdin of two strings.
# it takes that table and produces a new table 
# of each string in column 1 as rows, each string 
# of column 2 as column header and a 1/0 in each 
# cell for if that string from second column matches 
# the first column string
# So, a table of 
# 
#	jason	great
#	matt	good
#	jason	good
#	rimma	awesome
#	rimma	super
#	himanshu	awesome
#	rimma	good
#
# would give
#
#			great	good	awesome	super
#	jason	1	1	0	0
#	matt	0	1	0	0
#	rimma	0	1	1	1
#	himanshu	0	0	1	0
#

my %descs;
my %names;
my %combo;

while(<>){
	my($col1,$col2) = split;

	$descs{$col1} = 1;
	$names{$col2} = 1;
	
	$combo{$col1.":::".$col2} = 1;
}

my $header;
for my $head (sort(keys(%names))){
	$header .= "\t".$head;
}
print $header."\n";


for my $desc (keys(%descs)){
	
	print $desc;
	
	for my $name (sort(keys(%names))){
		
		if(exists($combo{$desc.":::".$name})){
			print "\t1";
		}
		else{
			print "\t0";
		}
	}
	
	print "\n";
}

exit;
