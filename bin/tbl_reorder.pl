#!/usr/bin/env perl
use strict;

my $desired = shift(@ARGV);

die "usage: cat tbl | reorder_col.pl col1,col5,col0,col2\n" unless defined($desired);

#with table input on stdin 
# output same table in diff order
#input is tbl on stdin, col to reorder as 
# cmd-line argument separated by comma
#skips comment lines '^##' entirely (vcf) now tbl

while(<STDIN>){
	next if /^\#\#/;

	my @col=split(/\t/,$_);
	$col[-1] =~ s/\n$//;

	if($desired !~ /,/){#only one col, make 1st and print all
		my $col0 = splice(@col,$desired,1);
		unshift(@col,$col0);

		print join("\t",@col)."\n";
	}
	else{
		print join("\t",@col[eval($desired)])."\n";
	}
}

exit;
