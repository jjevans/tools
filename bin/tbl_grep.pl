#!/usr/bin/env perl
use strict;

#print if specified file has pattern in column
#input is table/vcf on stdin
#prints if comment line "^#" regardless
#as arguments requires a pattern to match (quotes if nec)
#optional second arg is a column to match to, 
# default is column 1 (col[0])
die "usage: cat file.tbl | tbl_col_grep.pl pattern column(optional, default=column0)\nNOTE: column num starts at 0\n" unless @ARGV > 0;
my $pattern = shift;
my $column = shift;

$column = 0 unless defined($column);

while(<STDIN>){
	my @col = split(/\t/,$_);
	print if (/^\#/ || $col[$column] =~ /\Q$pattern\E/);
}

exit;

