#!/usr/bin/env perl
use strict;

#Merges two tables with common ids in the 
# first column.  Made specifically to include 
# cases of non-unique ids in the first table file.
#The second table must have unique ids or data 
# will be lost.  
#
#Outputs the same table as inputted (table1) 
# with the associated info appended in subsequent 
# columns in each line
#Third argument (1=yes) indicates that a "NONE" will 
# be printed in the last column of those lines having 
# an id in the first table file that does not exist 
# in the file having the associated info.
#
#Note: if no associated info, still prints the line 
# with "NONE" in the last column. Unless there is only 
# two columns in the associated info file, that means 
# there will be an inconsistent number of columns in 
# those lines. 
#
#Dies if id exists more than once in 
# file of ids to associate
#
# ex.
# file1:
# 	id1	ABC
# 	id2	DEF
# file2:
# 	id1	blahblah
# 	id2	blahblahblah
# 	id1	blah
# 	id1	umm
# 	id3	umm
# output:
# 	id1	blahblah	ABC
# 	id2	blahblahblah	DEF
# 	id1	blah	ABC
# 	id1	umm	ABC
# 	id3	umm	NONE
# 
my $null_val = "NONE";

die "usage: common_col_multi.pl main_table_file associated_info_file print_lines_without_associated_info(1=yes,optional)\n" if @ARGV < 2;
my $tblfile = $ARGV[0];
my $assocfile = $ARGV[1];

open(ASSOC,$assocfile) || die "Cannot open file of ids to associate\n";
my %assoc;
while(<ASSOC>){
	chomp;

	my($id,$info) = split(/\t/,$_,2);

	die "id exists multiple times in associated id file!: ".$id."\n" if defined($assoc{$id});

	$assoc{$id} = $info;
	
}
close(ASSOC);

open(TBL,$tblfile) || die "Cannot open table file\n";
while(<TBL>){
	chomp;

	print $_."\t";#print 1st cols plus tab

	#add associated info
	my($id,$irrelevant) = split(/\t/,$_,2);

	if(defined($assoc{$id})){
		print $assoc{$id}."\n";
	}
	else{
		print $null_val."\n";
	}
}
close(TBL);

exit;

