#!/usr/bin/env perl
use strict;

#NOTES:
# position based length of indel
#cat script_form1.lst | perl -ne 'chomp;/^(\d+):(\d+)(\D+)\/(\w+)$/;my $chr=$1;my $pos=$2;my $ref=$3;my $alt=$4;if(length($ref)>1){$pos.="-".eval($pos+length($ref)-1);print $chr.":".$pos.$ref."/".$alt."\n"}else{print $_."\n";}' > script_form2.lst


#format vcf or a tbl with the correct column 
# into trevor pugh's script format.
# format for coords
# SVN/ngs/variant-reporting/annotation/trunk/coords2lmmcds.py
#
#input form described in that script
#"Coordinates must be in the format chr:startA/B (variant), chr:start-endA/BB (insertion), or chr:start-endAAA/B (deletion).
#Multiple coordinates can be passed as a comma-separated list or as a path to a file containing a list of variants.
#When listed in a file, reference and variant bases can be separated by >, e.g. A>B."
my @outline;

die "usage: gi_hgvs_form.pl vcf_or_tbl_file\n" unless @ARGV == 1;

open(IN,$ARGV[0]) || die "Cannot open input file\n";
while(<IN>){
	next if /^\#/;#header
	chomp;
	
	my $line;
	
	my @col = split(/\t/,$_);
	my($chr,$pos,$id,$ref,$alt) = @col[0..4];

	#multiple alternates, print on separate lines
	#feed each allele as separate lines to form_indel()
	my @alts = split(/\,/,$alt);

	foreach my $allele (@alts){

		my($chr,$pos,$id,$ref,$alt) = @col[0..4];
		
		if($chr =~ s/^chr//){#remove chr from chromosome so fits geneinsight
			warn "WARNING: chromosome starts with 'chr', removing for compatibility. continuing...\n";
		}

		if(length($ref)>1){
			
			$pos .= "-".eval($pos + length($col[3])-1);
			#$line .= $chr.":".$pos.$ref."/".$allele."\n";
			
			#print $col[0].":".$col[1].$col[3]."/".$allele."\n";
		}
		
		push(@outline,$chr.":".$pos.$ref."/".$allele."\n");
	}

}
close(IN);

#print output
foreach my $row (@outline){
	print $row;
}

exit;
