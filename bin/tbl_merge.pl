#!/usr/bin/env perl
use strict;

#insert a table file into 
# another table file based 
# on common id in 1st column 
# and the column num to merge 
# into

#input two files and optionally a col num
die "usage: tbl_merge.pl file1.tbl file2.tbl colnum(optional, default append)\n" unless @ARGV > 1;
my $tbl1_file = $ARGV[0];
my $tbl2_file = $ARGV[1];
my $colnum = $ARGV[2];#default append

my $prev;#len previous line, enforces same num col in tbl2

#table 2
my %tbl2;
open(my $tbl2_fh,$tbl2_file) || die "ERROR: can't open 2nd file: ".$tbl1_file."\n";
while(<$tbl2_fh>){
	s/\n$//;
	
	my @col = split(/\t/,$_);
	my $id = shift(@col);
	#checking num col same from last line
	if(defined($prev) && @col != $prev){
		die "different number of columns in 2nd table file from last line, id: ".$col[0]."\n";
	}
	else{
		$prev = @col;
	}
	
	if(defined($tbl2{$id})){#previous id already exists
		warn "WARNING: Clobbering id in 2nd file: ".$tbl2_file.", id: ".$col[0]."\n";
	}
	
	$tbl2{$id} = \@col;
#	print "tbl2\t".$tbl2{$col[0]}."\t".join("###",@{$tbl2{$col[0]}})."\n";

}
close($tbl2_fh);


#table 1
open(my $tbl1_fh,$tbl1_file) || die "ERROR: can't open 1st file: ".$tbl1_file."\n";
while(<$tbl1_fh>){
	s/\n$//;
	
	my @col = split(/\t/,$_);
	my $id = shift(@col);
	
	#tbl2 array cols
	my $tbl2_insert;	
	if(defined($tbl2{$id})){
		$tbl2_insert = $tbl2{$id};
#		print "insert\t".$tbl2_insert."\t".join(":::",@{$tbl2_insert})."\n";
		#delete($tbl2{$id});
	}
	else{#no value in tbl2
#!!!not sure this if (insert empty array) works as my data didn't have this type of case

#		warn "WARNING: no value in 2nd table file: ".$col[0].", inserting undef arr.\n";
#		print "prev\t".$prev."\n";
		my @empty = (-1) x $prev;
		#my @empty = (undef) x $prev;
		$tbl2_insert = \@empty;
	}
		
#	print "to_splice\t".$tbl2_insert."\t".join("!!!",@{$tbl2_insert})."\n";
	#merge arrays
	$colnum = @col unless defined($colnum);
			
	splice(@col,$colnum,0,@{$tbl2_insert});

	print $id."\t".join("\t",@col)."\n";
}
close($tbl1_fh);

#warn if no val from 2nd tbl in 1st tbl
foreach my $unmatched (keys(%tbl2)){
#	warn "WARNING: no value in 1st table file: ".$unmatched."\n";
}
	
exit;
