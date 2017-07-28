#!/usr/bin/env perl
use strict;

#make unique id by combining specified columns by "|" 
# for inserted uniq id in 1st column
#to make input files for tbl_common.pl
#input table on stdin with column nums separated by "," 
# as 1st arg.  outputs table to stdout

#jje16, msl34	10242015
#partners personalized medicine, bioinformatics
my $delim = "|";
my $do_die = 0;#die on finding a duplicate id (all should be uniq)

#usage
print $ARGV[0]."\t".defined($ARGV[0])."\n";


if(!-z STDIN || !defined($ARGV[0])){
	print "usage: cat file.tbl | tbl_mkid.pl col_nums(by comma ex. 3,2,6)\n";
	exit;
}

#get desired columns and in same order from arg 1
my @cols = split(/,/,$ARGV[0]);

my %uniqs;
	
while(<STDIN>){
	my @arr=split(/\t/,$_);	\

	my $uniq_id;
	
	#loop over inputted col nums to keep desired order
	foreach my $col (@cols){
		$uniq_id .= $arr[$col].$delim;
	}
	
	#remove trailing delimiter
	$uniq_id =~ s/\Q$delim\E$//;

	#quick check to make sure new id is uniq in set
	if(defined($uniqs{$uniq_id})){
		
		my $message = "WARNING: multiple ids for 1st column are the same and are non-unique.\n";
		
		if($do_die){#exception
			die $message;
		}
		else{
			print STDERR $message;
		}
	}
	else{ $uniqs{$uniq_id} = 1; }
	
	print $uniq_id."\t".$_;
}

exit;
