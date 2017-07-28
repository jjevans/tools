#!/usr/bin/env perl
use strict;

#make key-value pairs of FORMAT id and each sample value
#jje16, msl34	10242015
#partners personalized medicine, bioinformatics

#match every value in each sample element (cell) 
# to its FORMAT id making key-value pairs of values in samples
#ex. 
# format:	GT:FS:CLASS
# orig sample:  0/1:0.4:benign
# final sample: GT=0/1:FS=0.4:CLASS=benign
#outputs vcf to stdout
#input is a vcf file on stdin

#usage
if(-t STDIN){#no stdin
	print STDERR "usage: vcf_keyval.pl (input vcf on stdin, output on stdout)\n";
	exit;
}

#iterate vcf
while(<STDIN>){

	if(/^\#/){#print header
		print;
	}
	else{#variant rows
		s/\n$//;
		my @col=split(/\t/,$_);
		my $format=$col[8];
		my @form=split(/:/,$format);

		#iterate each sample in each variant row
		for(my $i=9;$i<@col;$i++){

			if($col[$i] ne "."){
				my @newval;
				my @val=split(/:/,$col[$i]);

				#iterate each field in sample element
				#match FORMAT id to its value in each sample
				for(my $j=0;$j<@form;$j++){
					push(@newval,$form[$j]."=".$val[$j]);
				}
				
				#replace values of sample with key-value pairs
				$col[$i]=join(":",@newval);
			}
		}

		print join("\t",@col)."\n";
	}
}

exit;
