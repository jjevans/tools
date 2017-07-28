#!/usr/bin/env perl
use strict;


#gvcf to vcf
#jje16, msl34, biofx, personalized medicine, 05072015
#removes line with alt of <NON_REF> or "." (gvcf)
#with any arg it will remove nonref from multiallelic 
# valid alts.  default leaves nonrefs with valid alts
#removes all positions with alt of exactly "<NON_REF>"
my $nonref = "<NON_REF>";

my $filetype_chk = 1;#add fileformat line unless exists
my $filetype = "##fileformat=VCFv4.1";

#usage if no stdin
if(-t STDIN){
	die "usage: vcf_from_gvcf.pl rm_nonref_from_valid_alts (optional, any string, default do not rm)\n";
}

#check if ARGV has content
my $rm_nr = 0;
$rm_nr = 1 if defined(shift);

#add fileformat declaration if not present
my $line1 = <>;
print $filetype."\n" if ($filetype_chk && $line1 !~ /^\#\#fileformat=/);
print $line1;

while(<STDIN>){

	if(/^\#/){
		print
	}
	else{
		s/\n$//;
		my @col = split "\t";


		#skip gvcf lines != alt
		if($col[4] ne $nonref && $col[4] ne "."){
			
			if($rm_nr){#remove nonref from valid alts
				$col[4] =~ s/,?$nonref//g;
			}

			print join("\t",@col)."\n";
		}
	}
}

exit;

