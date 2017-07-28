#!/usr/bin/env perl
use strict;
use File::Slurp;

# from LRG xml output the LRG id, gene symbol, 
# and refseq transcript id
# prints "No major transcript found." if none found

die "usage: lrg_refseq.pl lrg_xml_file\n" unless @ARGV == 1;
my $lrg_xml = $ARGV[0];
my $xml = read_file($lrg_xml);


## default outputs
my $sym = "NoSymbolFound";
my $mrna;# later checks undef

## updatable annotation sets
my @anno_sets = split(/\<\/annotation_set\>\s*\<annotation_set\>/,$xml);

# remove all exterior information from 1st 
# (including fixed anno) and last sets
$anno_sets[0] =~ s/^.*\<annotation_set\>/\<annotation_set\>/;
$anno_sets[-1] =~ s/\<\/annotation_set\>.*$/\<\/annotation_set\>/;


## lrg id from beginning of file (first chunk)
$anno_sets[0] =~ /\<id\>(.+?)\<\/id\>/;
my $id = $1;

## get refseq anno set
foreach my $set (@anno_sets){

	# identify the refseq genes annotation set (source name)
	if($set =~ /\<name\>NCBI RefSeqGene\<\/name\>/){
		
		# split by gene 
		# (multiple genes because some partial genes overlap, but incorrect)
		my @genes = split(/\<\/gene\>\s*\<gene/,$set);

		# find gene with major transcript
		foreach my $gene (@genes){
			
			# major transcript
			if($gene =~ /\<transcript .*accession="(.+?)" .*fixed_id="t1"/){
				$mrna = $1;
				
				# gene symbol
				$gene =~ /\<symbol .*name="(.+?)"/;
				$sym = $1 unless $1 eq $mrna;# no match
			}
		}		
	}
}


## output
if(defined($mrna)){
	print $id."\t".$sym."\t".$mrna."\n";
}
else{
	print $id.": No major transcript found.\n"
}


exit;
