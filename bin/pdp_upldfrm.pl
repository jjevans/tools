#!/usr/bin/env perl

#!!!removes chr off chromosome if present

###column format for pdp uploadFRM to OMS
##creates a 19 column tab delim file 
# form OMS upload form.
##input is a standard form with 5 extra columns 
# at row end for genome coordinates
##no glitz, just assign old column nums 
# from old to new
my $num_col_orig = 19;#num col in orig upForm
my $num_col_coord = 5;#num col for genome coord cols

###column_name	old_uploadForm	new_uploadform
#GENE	1 -> 1
#Status	12 -> 2
#Status Date	13 -> 3
#Fwd Primer (Fa) 7 -> 4
#Fwd Sequence	8 -> 5
#Fwd SNP Check	14 -> 6
#Fwd SNP Check Date	15 -> 7
#Rev Primer (Ra)	9 -> 8
#Rev Sequence	10 -> 9
#Rev SNP Check 16 -> 10
#Rev SNP Check Date	17 -> 11
#Ext ?->Pair Type	12 -> 12
#Pair Chromosome	13
#Pair Start	14
#Pair Stop	15
#Pair Strand	16
#Pair Build	17
#Transcript	4 -> 18
#Notes	19 -> 19	


die "usage: form_col.pl pdp_uploadForm.txt output_file\n" unless @ARGV == 2;
my $form = $ARGV[0];
my $outfile = $ARGV[1];

open(OUT,">$outfile") || die "Cannot open file for result output\n";

open(FRM,$form) || die "Cannot open uploadForm.txt file\n";
while(<FRM>){
	chomp;
	my @col = split(/\t/,$_);
	my @new_col;foreach(@col){push(@new_col,"");}#forgot how to init arr of len
	
	#!!!take chr off chromosome num
	$col[19] =~ s/^chr//;
	
	$col[18] =~ s/^\d+\,//;#rm ampl size notes
	
	#fix col4 to have leading 0 on single digit
	my $exon_fix = fix_col4($col[4]);

	my $regname = $col[0].".".$exon_fix;#region name
	
	my @new_col = ($regname,@col[11,12,6,7,13,14,8,9,15,16,10,19,20,21,22,23,3,18]);

	print OUT join("\t",@new_col)."\n";

}
close(FRM);

close(OUT);

exit;

sub fix_col4{
	#add leading 0 to single digit exon name
	# accomodate alternate exons
	#change -CUT1 to c1 
	#	ex. 04A-CUT1 -> 04Ac1
	my $column4 = $_[0];
	
	#regex
	$column4 =~ s/-(\d)$/-0\1/;
	$column4 =~ s/-(\d\D+)$/-0\1/;
		
	#change 01-CUT1 -> 01c1
	$column4 =~ s/-CUT(\d+)$/c\1/;

	return $column4;
}