#!/usr/bin/env perl
use strict;

#break bedtools intersect 
#input is intersect left outer join (-loj)
#prints intersect result lines 
# not having same/similar id
#input is bedtools intersect results

#delimiters and element number for 
# id to split for substring to compare to 
# each other.
my $delim_a = "_";#bedfile a id delimiter
my $elemnum_a = 0;
my $delim_b;#compare whole id (do not split)
my $elemnum_b;#if so, undefined

die "usage: bt_isec_like_id.pl bedtools_isec_results\n" unless @ARGV == 1;

open(my $isec,$ARGV[0]) || die "cannot open bedtools intersect results file\n";
while(<$isec>){
	
	my @col = split(/\t/,$_);
	
	my $id_a = $col[3];
	$id_a = split_elem($id_a,$delim_a,$elemnum_a) if defined($delim_a);
	
	my $id_b = $col[9];
	$id_b = split_elem($id_b,$delim_b,$elemnum_b) if defined($delim_b);
	
	#print bedtools isec output
	print if $id_a eq $id_b;
}
close($isec);

#get id substrings to compare
sub split_elem{
	#split spltstr by delim and return colnum element (substring)
	my $spltstr = $_[0];
	my $delim = $_[1];
	my $colnum = $_[2];
	
	my @col = split($delim,$spltstr);
	
	return $col[$colnum];
}