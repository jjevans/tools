#!/usr/bin/env perl
use strict;

#look at the sample column from an 
# input vcf.  find if num vals in 
# sample coincide with the num vals 
# defined in FORMAT col.
#sample delimited by ":"
#input on stdin, output stdout
#optional arg of the sample col 
# to validate
my $form_col =  8;
my $smpl_col = 9;

die "usage: vcf_valid_form in_vcf out_vcf sample_column(optional)\n" unless @ARGV == 2;

$smpl_col = $ARGV[2] if defined($ARGV[2]);#optional

open(IN,$ARGV[0]) || die "bad input file\n";
open(OUT,">$ARGV[1]") || die "bad output file\n";

while(<IN>){

	if(/^\#/){
		print OUT $_;
	}
	else{
		chomp;

		my @col = split(/\t/,$_);
	
		my $form_val = $col[$form_col];
		my $smpl_val = $col[$smpl_col];
	
		#if !defined($smpl_val){
		#	warn "Error: sample column undefined: ".$col[0].":".$col[1].".\nvalue: ".$smpl_col."\n";
		#}
		
		my @format = split(/:/,$form_val);
		my @sample = split(/:/,$smpl_val);
		
		#num col check
		if(@format == @sample ){#good format vs sample
			print OUT $_."\n";
		}
		else{#bad sample col, STDOUT
			print "Error:\t".$_."\n";
		}
	}
}

close(OUT);
close(IN);

exit;