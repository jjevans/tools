#!/usr/bin/env perl
use strict;
use Bio::EnsEMBL::Slice;

die "usage: bed_to_gene.pl bed_file species output_file\n" unless @ARGV == 3;
my $bedfile = $ARGV[0];
my $species = $ARGV[1];
my $outfile = $ARGV[2];

# connect to db
my $registry = 'Bio::EnsEMBL::Registry';
$registry->load_registry_from_db(
    -host => 'ensembldb.ensembl.org', # alternatively 'useastdb.ensembl.org'
    -user => 'anonymous'
);

# set up db
my $slice_adaptor = $registry->get_adaptor($species, 'Core', 'Slice' );

open(BED,$bedfile) || die "cannot open bed_file at bed_to_gene.pl.\n";
open(OUT,">$outfile") || die "cannot open output_file at bed_to_gene.pl.\n";

while(<BED>){
	
	my @col = split;
	my $chr = $col[0];
	$chr =~ s/chr//i;
	my $start = $col[1];
	my $end = $col[2];

	
	# set up region
	my $slice = $slice_adaptor->fetch_by_region( 'chromosome',$chr,$start,$end);
	
	# get all genes in that region
	my $genes = $slice->get_all_Genes();
	
	# output bed
	foreach my $gene (@$genes){
		my $stable_id = $gene->stable_id();
		my $interval = join "\t",@col[0..2];
		
		print OUT $interval."\t".$stable_id."\n";
	}
}
	
