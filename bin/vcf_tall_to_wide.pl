#!/usr/bin/env perl
use strict;

#convert vcf from tall (multi line, one position 
# to wide (multi-allelic) format
#jje16, msl34, personalized medicine, biofx 05152015

#one pos/per line, collect all alts
#input is vcf on stdin, output vcf on stdout
#NOTE: when merging variants, if each line 
# has different content, all but one will be lost.

#usage if no stdin
if(-t STDIN){
	die "usage: vcf_tall_to_wide.pl (input vcf on stdin)\n"; 
}


my %pos;
my @order;
while(<STDIN>){
	
	if(/\#/){ print }
	
	else{
		s/\n//;
		my @col = split(/\t/,$_);
		
		my $id = $col[0].":".$col[1];
		
		if(!defined($pos{$id})){#init
			$pos{$id} = ["", []];
		}

		#add allele to alt (value: arr('curr alt A,G...', arr cols of variant)
		$pos{$id}[0] .= ",".$col[4];
		
		$pos{$id}[1] = \@col;
			
		push(@order,$id);
	}
}

foreach my $id (@order){
	if(defined($pos{$id})){

		my $alt = $pos{$id}[0];
		$alt =~ s/^,//;
		
		$pos{$id}[1]->[4] = $alt;
	
		my $line = join("\t",@{$pos{$id}[1]});
		print $line."\n";
		
		delete($pos{$id});
	}
}

die "ERROR: leftover keys, somethings wrong." if keys(%pos) > 0;

exit;
