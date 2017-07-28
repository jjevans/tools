#!/usr/bin/env perl
use strict;

#remove a sample from a vcf


die "vcf_rm_smpl.pl vcf_file column_number\n" unless @ARGV == 2;
my $vcf = $ARGV[0];
my $colnum = $ARGV[1];

open(my $vcf_fh,$vcf) || die "cannot open vcf file\n";
while(<$vcf_fh>){

	if(/^\#\#/){ print }
	else{
		my @col = split(/\t/,$_);
		$col[-1] =~ s/\n$//;

		splice(@col,$colnum,1);

		print join("\t",@col)."\n";
	}
}
close($vcf_fh);

exit;

