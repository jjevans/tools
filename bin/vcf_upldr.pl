#!/usr/bin/env perl
use strict;

#jje16, msl34 05242015
#partners personalized medicine, bioinformatics
#pull info fields from vcf from a file of desired INFO fields
# and join them all together in one string for each allele
#system call to vcftools
#input is downloaded exac (or any) vcf and a one column file of INFO ids (etc QD)
my $id = "EXAC";#our INFO id

#usage
die "usage: vcf_upldr.pl vcf file_of_INFO_ids_in_1col\n" unless @ARGV >= 2;
my $vcf = $ARGV[0];
my $flds_file = $ARGV[1];
$id = $ARGV[2] if defined($ARGV[2]);

#build INFO definition to insert into header.  
#inserts INFO def and version string if provided immediately before the 
# true header line '#CHROM'.
my $desc = "Population frequencies. Format: ";
my $delim = "|";
my $def = '##INFO=<ID='.$id.',Number=.,Type=String,Description="';

#file of desired fields
my @ids = ("REF","ALT");

open(my $flds_fh,$flds_file) || die "Cannot open file with list of INFO fields to extract.\n";
while(<$flds_fh>){
	chomp;
	push(@ids,$_);
	print "yo\t".$_."\n";
}
close($flds_fh);

$desc .= join($delim,@ids).'">';
$def .= $desc."\n";

#vcf
open(my $vcf_fh,$vcf) || die "Cannot open VCF to convert.\n";
while(<$vcf_fh>){

	if(/\#/){#header

		print $def if /\#CHROM/;			
		print;
	}
	else{#variants
		my @col = split(/\t/,$_);
		$col[-1] =~ s/\n$//;
		
		#alleles
		my @alts = split(/,/,$col[4]);

		#make arr of strings for each allele, init with ref, alt
		my @strs;#new info strs
		foreach my $alt (@alts){
			
			my $ref = $col[3];
			my $str = $ref.$delim.$alt;
			
			push(@strs,$str);
		}


		my $icol = $col[7];
		my @all_flds = split(/\;/,$icol);

		my $num_found = 0;
		
		foreach my $fld (@all_flds){
			my($id,$value) = split(/=/,$fld);

			#get desired field
			if($id ~~ @ids){


				#go through each value, delim by ',' if mutiallelic
				my @vals = split(/,/,$value);

				#assess that num values in field works for each allele
				if(@vals == 1){#one value, use for all alleles
					my $val = pop(@vals);
					@vals = ($val) x @alts;
				}
				elsif(@vals != @alts){#something's wrong
					my $message = "Error: number of alternate alleles different than the number of values in INFO field: ".$fld."\n -- position: ".$col[0].":".$col[1]."\tnum allele: ".@alts.", num values: ".@vals.", note: 1 value ok\n";
					die $message;
				}


				#add values to each allele str
				for(my $i=0;$i<@alts;$i++){
					$strs[$i] .= $delim.$vals[$i];
				}
				
				$num_found++;
			}
		}

		#check all fields found or die
		if($num_found != (@ids-2)){#no REF, ALT
			my $message = "ERROR: ".$col[0].":".$col[1].", required number of fields was not found.  desired: ".eval(@ids-2).", found: ".$num_found."\n";
			die $message;
		}

		#rm lead delim
		foreach my $str (@strs){
			$str =~ s/^\Q$delim\E//;
		}

		$col[7] = $id."=".join(",",@strs);

		print join("\t",@col)."\n";
	}

}
close($vcf_fh);

exit;
