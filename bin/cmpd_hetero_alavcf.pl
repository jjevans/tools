#!/usr/bin/env perl
use strict;

#from alamut vcf used for WGS uploader (will be different 
# in WES), pull out all variants (by position) that are 
# in the same transcript.
# Prints if the variant is located with 
# at least one other variants in a transcript 
# for compound heterozygosity.
#prints each of transcript's vcf lines as output
#print triple equal (===) as delimiter between transcripts
# along with the transcript id and then its variants
my $delim = "===";

my $num_req = 2;#num variants required within transcript, default=2
my $print_header = 0;#print vcf header lines (1) or not (0)

die "usage: cmpd_hetero_alavcf.pl wgs_ala.vcf num_variants_required_per_transcript(optional,default=2)\n" unless @ARGV >= 1;
$num_req = $ARGV[1] if defined($ARGV[1]);

my %tids;#variants for each transcript id

open(ALAVCF,$ARGV[0]) || die "Cannot open wgs alamut vcf file\n";
while(<ALAVCF>){
	
	if(/^\#/){#vcf header lines
		print if $print_header;
	}
	else{
		my @col = split(/\t/,$_);
	
		$col[-1] =~ /^.*Transcript_Fields=(.+?)\|.*$/;
		my $id = $1;

		$tids{$id} = [] unless defined($tids{$id});#init array
	
		push(@{$tids{$id}},$_);
	}
}

foreach my $key (keys(%tids)){
	if(@{$tids{$key}} >= $num_req){
		print $delim.$key."\n";#print delimiter and transcript id
		
		foreach my $vcfline (@{$tids{$key}}){
			print $vcfline;
		}
	}
}

exit;
