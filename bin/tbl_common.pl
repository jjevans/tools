#!/usr/bin/env perl
use strict;

###
#   common_col.pl
#   JJE, 07.18.2011
#
###

# finds the lines having first column (presumably an id) common in two files
#       effectively merges contents of two files by id
#   does not account for duplicate entries in the same file.
my $both = 1;#join both files data on each line
my $message = "usage: common_col.pl file1 file2 merge_both_file_data(optional,default true (1)),any 3rd arg value prints only file1 contents.\n";
die $message unless exists $ARGV[0] && exists $ARGV[1];

my $f1 = $ARGV[0];
my $f2 = $ARGV[1];
$both = 0 if defined($ARGV[2]);

my @ordr;

# go through first file and load of hash by first column values as keys
my %f1_words;
open(my $f1_fh,$f1) || die "Cannot open first file: ".$f1." .\n";
while(<$f1_fh>){
   my @words = split(/\t/,$_);
   $words[-1] =~ s/\n$//;#chomp

   my $id = shift(@words);

   $f1_words{$id} = join("\t",@words);

   push(@ordr,$id);
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
foreach my $id (@ordr){
#foreach my $key (keys(%f1_words)){
   if(defined($f1_words{$id}) && defined($f2_words{$id})){

      #print
      my $line = $id."\t".$f1_words{$id};

      if($both){#merge both file data on one line
         $line .= "\t".$f2_words{$id} if $f2_words{$id} ne "";
      }

   #   $line =~ s/\t$//;
      print $line."\n";
   }
}

exit;
