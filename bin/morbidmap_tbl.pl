#!/usr/bin/env perl 
use strict;

# parse omim morbidmap file into a tab delimited file for a database

# output is table as
# pheno description<tab>pheno id<tab>gene symbol<tab>omim gene id<nl>
# if no pheno id for description gives NULL (for db field)
# omim gene id will not be unique (multiple rows with same id)
my $none = "NULL";

die "usage: morbidmap_tbl.pl OMIM_morbidmap_file\n" unless @ARGV == 1;

open(MM,$ARGV[0]) || die "cannot open morbidmap file\n";
while(<MM>){
	my @cols = split(/\|/,$_);
	
	# get omim id and description (col1)
	$cols[0] =~ s/[\?\{\}\[\}]//g;# get rid of ?,[,{,],}
	$cols[0] =~ s/ *\(\d+\) *$//;# get rid of evidence code ex."(3)"

	my @fields = split(/\, /,$cols[0]);
	my $id = $none; # if no pheno id present
	$id = pop(@fields) if $fields[-1] =~ /^\d{6}$/;# change var to pheno id if present
	my $desc = join ", ",@fields;# rejoin the description

	# pull off first gene symbol (current symbol) from list of past and present symbols
	my @syms = split(/\, /,$cols[1]);
	my $sym = $syms[0];
	
	# print output
	print $desc."\t".$id."\t".$sym."\t".$cols[2]."\n";
}
close(MM);

exit;
