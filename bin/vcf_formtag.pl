#!/usr/bin/env perl
use strict;

#add format tags to each sample's value 
# by making them key value pairs.

#ex.
# format = RS:ML:HS:ET
# sample = 1:2:3:4
# default output in each sample col = 
# RS=1:ML=2:HS=3:ET=4

#input and output are vcf format
#!dies if not enough cols given $tag_col (no val cols)
#!dies if the num tags != num vals 

##runtime vars
my $print_head = 1;#print header
my $warn_or_die = 1;#die (1) if @tags!=@vals

#output each smpl field by this delim
my $smpl_delim_out = ":";

#col with tags (format), samples thereafter
my $tag_col = 8;

#die "usage: vcf_tag_keyval.pl (stdin->stdout)\n\toptional arg indicates the \n column number of the tags\n where all following columns are samples.\n\n" unless @ARGV >= 2;
die "usage: vcf_tag_keyval.pl vcf_file tag_col_num(optional,default 8,0-based)\n" unless @ARGV > 0;
my $infile = $ARGV[0];
#my $outfile = $ARGV[1];
$tag_col = $ARGV[1] if $ARGV[1];


open(IN,$infile) || die "Cannot open input vcf file.\n";
#open(OUT,">$outfile") || die "Cannot open output vcf file.\n";
#select(OUT);#prints to file

while(<IN>){
	if($print_head && /^\#/){
		print;
	}
	else{
		s/\n$//;

		my @col_smpl=split(/\t/,$_);#ends up just the samples
		my @col_vcf = splice(@col_smpl,0,($tag_col-1));
		my $col_tag = shift(@col_smpl);

		#output, init the vcf's first columns
		my $outstr = join("\t",@col_vcf);

		if(@col_smpl < 1){#not enough columns
			die "Error: not enough columns in file to work with.\nColumn with tags: ".$tag_col."\n";
		}
		else{

			#tags
			my @tags = split(":",$col_tag);

			for(my $i=0;$i<@col_smpl;$i++){
				
				if($col_smpl[$i] eq "."){
					$outstr .= "\t".$col_smpl[$i];
				}
				else{

					my @vals = split(/:/,$col_smpl[$i]);
			
					if(@tags != @vals){
						my $errstr = "sample number: ".$i.", different number of values in sample column than tags in tag column at vcf_formtag.pl::keyval()\n\tnum tags: ".@tags."\n\ttags: ".join(":",@tags)."\n\tnum values: ".@vals."\n\tvalues: ".join(":",@vals)."\n!";

						if($warn_or_die){
							die "!ERROR: ".$errstr."\n";
						}
						else{
							warn "!WARNING: ".$errstr."\n";
							$outstr .= "\tERROR";
						}
					}
					else{
						my $pairs = keyval(\@tags,\@vals);

						$outstr .= "\t".join($smpl_delim_out,@$pairs);
					}
				}
			}
		
			print $outstr."\n";
		}
		
	}		
}

#close(OUT);
close(IN);

exit;


sub keyval{
	#return key value pairs 
	# (str1=str2)
	#from two inputted arrays 
	# of EXACT SAME LENGTHS returns
	# array of key value 
	my $tags = $_[0];
	my $vals = $_[1];

	my @pairs;
	for(my $i=0;$i<@{$tags};$i++){
		my $pair = $tags->[$i]."=".$vals->[$i];

		push(@pairs,$pair);
	}
		
	return \@pairs;
}
