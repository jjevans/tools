#!/usr/bin/env perl
use strict;

#remove inputted FORMAT id from FORMAT 
# and the sample column.
#input is a vcf file
#output is stdout
my $frmt_colnum = 8;#col num of FORMAT

die "usage: vcf_rm_format.pl file.vcf tag_to_rm (ex. DP,AC)\n" unless @ARGV == 2;
my $vcffile = $ARGV[0];
my $tag = $ARGV[1];

my $line1 = 1;#boo if 1st variant line
my $header;

my $colnum;
my $frmt_tag_str;


open(VCF,$vcffile) || die "Cannot open input VCF file.\n";
while(<VCF>){

	if(/^\#/){
		$header .= $_ unless /^\#\#FORMAT=\<ID=$tag,/;#skip declaration of tag to rm
	}
	else{
	
		s/\n//;
		my @col = split(/\t/,$_);

		if($line1){#1st variant line
			
			#get column number of tag
			my @frmt_tags = split(/:/,$col[$frmt_colnum]);
			
			for(my $j=0;$j<@frmt_tags;$j++){

				if($frmt_tags[$j] eq $tag){#found desired tag to rm
					$colnum = $j;

					splice(@frmt_tags,$j,1);#rm tag from format col
					$frmt_tag_str = join(":",@frmt_tags);

					$j = @frmt_tags;#break out
				}
			}
			
			#die if no tag in FORMAT column
			if(!defined($colnum)){
				die "ERROR: requested tag not found in FORMAT column fields.\t".$tag."\n";
			}
			
			print $header;
			
			$line1 = 0;#only for 1st variant
		}
		
		#splice out tag value
		if(@col <= $frmt_colnum){#not enough columns, no samples
			warn "No samples exist for value removal.\n";
		}
		else{

			#iter from format through all samples
			for(my $i=$frmt_colnum+1;$i<@col;$i++){
				my @val = split(":",$col[$i]);

				splice(@val,$colnum,1);
				$col[$i] = join(":",@val);
			}
			
			$col[$frmt_colnum] = $frmt_tag_str;
			
			print join("\t",@col)."\n";
		}	
	}
}
close(VCF);

exit;
