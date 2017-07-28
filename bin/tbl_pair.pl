#!/usr/bin/env perl
use strict;

# merges values of 2 tables by header.
# Takes column with same header value 
# and compares the values having the 
# same id in the first column.
# Outputs a table with same header 
# and values for each table by 
# column by id with values delimited 
# by triple colon (:::).
# only merges columns with like header 
# values in both files and ids existing 
# in both files. the rest are excluded.
# Requires a header line in each table.
# Each line need have same number of columns.
# Requires unique ids in 1st col 
# (only 1 id per table).
# Prints output columns with id in first column 
# and with no order to columns in rest of tables
# (has header with column names in output)
# Prints original column name of id field (1st col) 
# from the first table file in output.

die "usage: merge_tbls.pl table1 table2\n" unless @ARGV == 2;


#table1
open(TBL1,$ARGV[0]) || die "cannot open first table file.\n";
my @t1 = <TBL1>;
close(TBL1);

my $head1_line = shift(@t1);

my $id_name = &id_colname($head1_line);

my $head1 = &break_head($head1_line);
my $vals1 = &break_tbl(\@t1);


#table2
open(TBL2,$ARGV[1]) || die "cannot open second table file.\n";
my @t2 = <TBL2>;
close(TBL2);

my $head2 = &break_head(shift(@t2));
my $vals2 = &break_tbl(\@t2);


#pair column names
my $paired_names = &pair_colnames($head1,$head2);

#pair column values
my $paired_values = &pair_vals($paired_names,$vals1,$vals2);

# print header ("id" is 1st column name), break after 1st iteration
foreach my $headid (keys(%$paired_values)){#just take header names from first id

	print $id_name;
	
	foreach my $name (sort(keys(%{$paired_values->{$headid}}))){
		print "\t".$name;
	}
	
	print "\n";
	
	last;
}

# print rest of table
foreach my $id (keys(%$paired_values)){

	print $id;

	foreach my $name (sort(keys(%{$paired_values->{$id}}))){
		print "\t".$paired_values->{$id}{$name};
	}
	
	print "\n";
}


exit;


sub id_colname{
	#get column name of id field (1st column) 
	# from inputted header line
	my $head_line = $_[0];
	
	my @colnames = split(/\t/,$head_line);
	my $id_name = shift(@colnames);
	
	return $id_name;
}
	
sub break_head{
	#return hash with 
	# header name as key, 
	# column number as value
	my $head_line = $_[0];
	
	chomp($head_line);
	my @cols = split(/\t/,$head_line);
	shift(@cols);#get rid of column name in 1st col (id colname)
	
	my %head_hsh;
	for(my $i=0;$i<@cols;$i++){
		$head_hsh{$cols[$i]} = $i;
	};
	
	return \%head_hsh;
}

sub break_tbl{
	#return hash with 
	# id (1col value) as key,
	# array of col values by 
	# column as value
	my $tbl = $_[0];
	
	my %tbl_hsh;
	for(my $i=0;$i<@$tbl;$i++){
		chomp($tbl->[$i]);
		
		my @cols = split(/\t/,$tbl->[$i]);

		my $id = shift(@cols);
		$tbl_hsh{$id} = \@cols;
	}
	
	return \%tbl_hsh;
}

sub pair_colnames{
	#from two hashes of names as key 
	# and column number as value 
	# create a hash having col name 
	# as key and an array having two 
	# elements of column number of first 
	# header hash as first element and column 
	# number of second hash as second element.
	# Only pairs col names existing in both 
	# hashes and ignores the rest.
	my $head_hsh1 = $_[0];
	my $head_hsh2 = $_[1];
	
	my %paired;
	foreach my $colname (keys(%$head_hsh1)){
	
		if(exists($head_hsh2->{$colname})){
			$paired{$colname} = [];
			$paired{$colname}[0] = $head_hsh1->{$colname};
			$paired{$colname}[1] = $head_hsh2->{$colname};
		}
	}
	
	return \%paired;
}

sub pair_vals{
	#using a hash of header names as key and column numbers 
	# in array of length 2 as values (from &pair_colnames), 
	# pairs column values together delimited by triple 
	# colon. returns a hash with id as key and paired 
	# value string as value.
	my $colnames = $_[0];
	my $vals1 = $_[1];
	my $vals2 = $_[2];
	my $delim = ":::";
	
	my %paired;
	
	foreach my $id (keys(%$vals1)){
	
		if(exists($vals2->{$id})){
		
			$paired{$id} = {};
			foreach my $name (keys(%$colnames)){
				my $colnum1 = $colnames->{$name}[0];
				my $colnum2 = $colnames->{$name}[1];
		
				my $v1 = $vals1->{$id}[$colnames->{$name}[0]];
				my $v2 = $vals2->{$id}[$colnames->{$name}[1]];
				
				#create hash by id with hash of colnames as key and delimited string as value 
				$paired{$id}{$name} = $v1.$delim.$v2;
			}
		}
	}
	return \%paired;
}
