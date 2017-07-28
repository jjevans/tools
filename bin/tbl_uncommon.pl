#!/usr/bin/perl
use strict;

###
#   uncommon_col.pl
#   JJE, 07.18.2011
#
###

#finds the lines having first column (presumably an id) 
# in 1st file and not in 2nd file 
#effectively prints contents of 1st file if not 
# in the 2nd
#   does not account for duplicate entries in the same file.
my $message = "usage: uncommon_col.pl file1 file2\n";
die $message unless exists $ARGV[0] && exists $ARGV[1];

my $f1 = $ARGV[0];
my $f2 = $ARGV[1];

# go through first file and load of hash by first column values as keys
my %f1_words;
open(my $f1_fh,$f1) || die "Cannot open first file: ".$f1." .\n";
while(<$f1_fh>){
   my @words = split(/\t/,$_);
   $words[-1] =~ s/\n$//;#chomp

   my $id = shift(@words);

   $f1_words{$id} = join("\t",@words);
}
close($f1_fh);

# load another hash with second file's first column contents as key
my %f2_words;
open(my $f2_fh,$f2) || die "Cannot open second file: ".$f2." .\n";
while(<$f2_fh>){
   my @words = split(/\t/,$_);
   $words[-1] =~ s/\n$//;#chomp

   my $id = shift(@words);

   $f2_words{$id} = join("\t",@words);
}
close($f2_fh);

# print any entry that has a common key in each hash
foreach my $key (keys(%f1_words)){
   unless(defined($f2_words{$key})){

      #print
      print $key."\t".$f1_words{$key}."\n";
   }
}

exit;
