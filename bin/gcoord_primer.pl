#!/usr/bin/env perl
use strict;

#from a table of primers 
# provide the genomic coordinates 
# of the target amplicon.
#uses e-pcr to get coordinates
#inputted table file is 3 columns 
# wide of primer pair id, left seq, 
# right seq.
#prints a bedfile of coords 
# and the primer pair id

die "usage: gcoord_primer.pl primer_table_file genome_fasta\n" unless @ARGV == 2;
my $prmrfile = $ARGV[0];
my $genome = $ARGV[1];
 