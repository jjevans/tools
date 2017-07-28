#!/usr/bin/env perl
use strict;

#order a table by id from a different list 
# file specifying the order
my $sort = 1;
my $sortcol = 0;#default first col

#input is a table to order, and a list file 
# having correct order
die "usage: tbl_order.pl tablefile order_list_file column_to_sort_by(optional, default col1)\n" unless @ARGV > 1;
my $tbl = $ARGV[0];
my $lst = $ARGV[1];
$sortcol = $ARGV[2] if defined($ARGV[2]);
$sort = 0 if $sortcol !~ /^\d+$/;

my %data;

open(TBL,$tbl) || die "cannot open table file: ".$tbl."\n";
while(<TBL>){
	s/\n$//;

	my @col = split(/\t/,$_);
	my $id = $col[$sortcol];
	
	if(!exists($data{$id})){
		$data{$id} = ();
	}

	push(@{$data{$id}},\@col);
}
close(TBL);

open(LST,$lst) || die "cannot open order list file: ".$lst."\n";
while(<LST>){
	chomp;
	my($id,$rest) = split(/\s/,$_,2);

	if(exists($data{$id})){
		my $outarr = \$data{$id};

		if($sort){
			$outarr = sort_by_col($outarr,$sortcol);	
		}

		print join("\n",@{$outarr})."\n";
	}	
}
close(LST);

exit;

sub sort_by_col{
	#given a 2-d array, 
	# use the inputted col 
	# and sort the array 
	# numerically and return 
	# a ref to new arr
	my $arr = $_[0];
	my $sortcol = $_[1];

	my %entry;	
	while(@$arr){
		my $sortval = $_->[$sortcol];

		if(!exists($entry{$sortval})){
			$entry{$sortval} = ();

		}

		push(@{$entry{$sortval}},$_);
	}
	
	my @res;

	foreach my $key (sort numerically(keys(%entry))){
		push(@res,$entry{$key});
	}

	return \@res;
}

exit;

sub numerically { $a<=>$b }

