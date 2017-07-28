#!/usr/bin/env perl
use strict;

# from two files presumably from the same software, 
# but of different versions, compare the table for 
# any differences.  Input to each of these file outputs 
# is assumed to be from the same input file so the 
# values will be the same if no change between first 
# and second versions.
#
# This tool compares three things:
#	1. if there are different header values
#		optional 3rd arg to specify whether 
#		header present
#	2. if there are different numbers of columns
#	3. if the values for each field are different
#

die "usage: compare_tbl.pl tbl_file1 tbl_file2 header_present(optional)\nIf a header is not present don't provide a 3rd argument\n" unless @ARGV > 1;

# first table
open(TBL1,$ARGV[0]) || die "Cannot open first table file.\n";
my @tbl1 = <TBL1>;

# second table
open(TBL2,$ARGV[1]) || die "Cannot open second table file\n";
my @tbl2 = <TBL2>;

# header
if(defined($ARGV[2])){
	my $head1 = shift(@tbl1);
	my $head2 = shift(@tbl2);
	
	chomp($head1);
	my $fields1 = &load_hash($head1);
	
	chomp($head2);
	my $fields2 = &load_hash($head2);
	
	($fields1,$fields2) = &elim_common($fields1,$fields2);
	
	foreach my $field (keys(%$fields1)){
		print $field."\n";
	}
}

exit;

sub load_hash{
	# from a tab delim string, 
	# return a hash with each column field as 
	# key and the column number as value
	
	my @cols = split(/\t/,$_[0]);
	
	my %fields;
	for(my $i=0;$i<@cols;$i++){
		$fields{$cols[$i]} = $i;
	}
	
	return \%fields;
}

sub check_head{
	# check header
	# return what column names differ and their column number
	
	my @cols1 = split(/\t/,$_[0]);
	my %vals1;
	for(my $i=0;$i<@cols1;$i++){
		$vals1{$cols1[$i]} = $i;
	}
	
	my @cols2 = split(/\t/,$_[1]);
	my %vals2;
	for(my $i=0;$i<@cols2;$i++){
		$vals2{$cols2[$i]} = $i;
	}
	
	
}

sub elim_common{
	# from two hash refs, remove all entries common to both hashes
	# returns the two hash refs back in the same order passed in
	my $hsh1 = $_[0];
	my $hsh2 = $_[1];
	
	# get rid of keys common to both hashes
	for my $key (keys(%$hsh1)){
		if(exists($hsh2->{$key})){
			delete($hsh1->{$key});
			delete($hsh2->{$key});
		}
		else{
			print "what ".$key."\n";
		}
	}
	
	return($hsh1,$hsh2);	
}
