#!/usr/bin/env perl
use strict;

#jje16, msl34	07212015
#from output of merge_tbls.pl find any two values 
# in a tbl cell that differ.
#input like:
#id0	2:::2	3:::3	4:::4
#id1	2:::2	3:::3	4:::4
#id2	2:::2	3:::1	4:::4
#
#id2 line would print output format 
#id<\t>raw value<\t>row number<\n>

die "usage: merge_tbls_diff.pl (merge_tbls.pl output on stdin)\n" if -t *STDIN;

my $head = "id\tvalue\tcol_num\n";
my $output;

while(<STDIN>){
	my @col = split(/\t/,$_);
	$col[-1] =~ s/\n$//;
	my $id = shift(@col);


	#iterate all values
	for(my $i=0;$i<@col;$i++){
		my($val0,$val1) = split(/:::/,$col[$i]);

		if($val0 ne $val1){

			$output .= $id."\t".$col[$i]."\t".eval($i+1)."\n";
		}
	}
}

if(defined($output)){
	print $output;
}
exit;

