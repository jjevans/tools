#!/usr/bin/env perl
use strict;

my $class="DM";
$class = shift(@ARGV) if @ARGV>0;

while(<STDIN>){
next if /^\#/;
my @col=split(/\t/,$_);
$col[-1]=~s/\n$//;

my $id = $col[2];
my @flds=split(/\;/,$col[7]);

my %ihsh;
foreach my $fld (@flds){
my($iid,$ival)=split(/=/,$fld);
die "Exists: ".$id."\t".$iid."\n" if defined($ihsh{$iid});
$ihsh{$iid}=$ival;
}

foreach my $mid (keys(%ihsh)){
if(!defined($ihsh{"CLASS"})){
	die "ain't got no CLASS: ".$id."\t".$mid."\n";
}
elsif($ihsh{"CLASS"} eq $class){
	$ihsh{"PHEN"} =~ s/\"//g;
	print $id."\t".$ihsh{"CLASS"}."\t".$ihsh{"GENE"}."\t".$ihsh{"DNA"}."\t".$ihsh{"PHEN"}."\n";
	last;
}}
}
exit;

