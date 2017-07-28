#!/usr/bin/env perl
use strict;

die "usage: compare_cols.pl tbl_file1 tbl_file2\n" unless @ARGV == 2;

# first table
open(TBL1,$ARGV[0]) || die "Cannot open first table file.\n";
my @tbl1 = <TBL1>;

# second table
open(TBL2,$ARGV[1]) || die "Cannot open second table file\n";
my @tbl2 = <TBL2>;


# go through each column of first table, 
# find column with same header id in the second table 
# as that column in the first table.
# compare values in column
my $head1 = shift(@tbl1);
chomp($head1);
my @colnames1 = split(/\t/,$head1);

my $head2 = shift(@tbl2);
chomp($head2);
my @colnames2 = split(/\t/,$head2);

for(my $i=0;$i<@colnames1;$i++){

	# col num in tbl2 for this tbl1 col,-1 default
	my $colnum = -1;
	
	for(my $j=0;$j<@colnames2;$j++){
		$colnum = $j if $colnames1[$i] eq $colnames2[$j];
	}
	
	if($colnum != -1){# column found in tbl2

		# get all column values for each file
		my @colvals1 = &col_arr(\@tbl1,$i);
		my @colvals2 = &col_arr(\@tbl2,$colnum);

		# compare values to see if different
		# get row nums where they differ
		my $diffrows = &eval_vals(\@colvals1,\@colvals2);
		
		print "ValDiffer:\t".$i."::".$colnames1[$i]."\t".join(",",@$diffrows)."\n";
	}
	else{
		print "ColUnmatched:\t".$colnames1[$i]."::".$i."\n";
	}
	
}

exit;

sub col_arr{
	# get all of the values for a column in from an array 
	# of tab delim strings.  return an array of values
	my $tbl = $_[0];
	my $colnum = $_[1];

	my @vals;
	foreach my $line (@$tbl){
		chomp($line);
		my @cols = split(/\t/,$line);
		
		push(@vals,$cols[$colnum]);
	}
	
	return @vals;
}

sub eval_vals{
	# check to see if elements in two arrays differ and 
	# report the element nums that do
	my $vals1 = $_[0];
	my $vals2 = $_[1];
	
	my @diffrows;
	for(my $i=0;$i<@$vals1;$i++){
		push(@diffrows,$i.":".$vals1->[$i].":".$vals2->[$i]) if $vals1->[$i] ne $vals2->[$i];
	}
	
	return \@diffrows;
}