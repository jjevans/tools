#!/usr/bin/env perl

# from merged table file (output of merge_tbls.pl) and the column 
# name desired, print the id column (column 1) and the column having 
# the column name (from header).  Does not print a header.

die "usage: tbl_colbyname.pl file_with_header.tbl column_name\n" unless @ARGV == 2;

open(MERGE,$ARGV[0]) || die "cannot open merge table file\n";
my $colname = $ARGV[1];

my @lines = <MERGE>;

my $headline = shift(@lines);
my $colnum = &colname_to_colnum($headline,$colname);

if($colnum >= 0){
	
	foreach my $line (@lines){
		chomp($line);
		
		my @cols=split(/\t/,$line);
		
		print $cols[0]."\t".$cols[$colnum]."\n";
	}
}
else{
	print STDERR "Column name not found: ".$colname."\n";
}

exit;


sub colname_to_colnum{
	#get column number of tab-delimited line having that string
	my $line = $_[0];
	my $desired = $_[1];
	
	chomp($line);
	my @colnames = split(/\t/,$line);

	my $colnum = -1;
	for(my $i=0;$i<@colnames;$i++){
		
		if($colnames[$i] eq $desired){
			$colnum = $i;
			$i=@colnames;
		}
	}
	
	return $colnum;
}
