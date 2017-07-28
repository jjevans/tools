#!/usr/bin/perl
use strict;

###
#   uncommon_id.pl
#   JJE, 07.18.2011
#
###

# find the lines with first column (id most likely) in file1 not existing in 
#       file2 first column.  Meant to report those ids that only exist in one file 
#       and not the other.
# does not handle the case of multiple lines with same first column id.  If
# there are duplicate ids only one will be reported
# prints out the lines with ids uncommon to both files.  if any argument 3 
# provided then prints both file1 and file2 ids that do not exist in their
# complement files.  Defaults to only printing those ids from file1 not existing 
# in file2

# input is file1 and file2 to compare first columns of
die "usage: uncommon_col.pl file1 file2\n" unless exists $ARGV[0] && exists $ARGV[1];

# load hash with file1 contents.  first column is key to compare with other file
my %f1_words;
open(F1,$ARGV[0]) || die "Cannot open first file: ".$ARGV[0]." .\n";
while(<F1>){
   chomp;
   my($word,$others) = split(/\t/,$_,2);

   $f1_words{$word}++;
}
close(F1);

# load second hash with file2 contents.  Ordered by key of first column id
my %f2_words;
open(F2,$ARGV[1]) || die "Cannot open second file: ".$ARGV[1]." .\n";
while(<F2>){
   chomp;
   my($word,$others) = split(/\s/,$_,2);

   $f2_words{$word}++;
}
close(F2);

# print those ids from first hash with first column id not in second hash
foreach my $key (sort keys(%f1_words)){
   print $key."\n" unless exists $f2_words{$key};
}

# if an argument 3 is provided then print out the ids from the second file also
if(defined $ARGV[2]){
        foreach my $key (sort keys(%f2_words)){
        print $key."\n" unless exists $f1_words{$key};
        }
}

exit;
