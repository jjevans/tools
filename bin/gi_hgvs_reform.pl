#!/usr/bin/env perl
use strict;

#take hgvs for each alt separated 
# in order to run trevor pugh's 
# script coords2lmmcds.py. 
#prints out a pretty table by 
# variant position
#input is a file of output from the script
# reconstructs vcf coords
#optional 2nd arg provides a delimiter 
# for the variant_id (with pipe, chrom|pos|refallele)
# #!! == hard-coded value
my $delim = "|";#!!internal delimiter
my $null_val = ".";#!!or "","NA"

#print new header to STDOUT/STDERR 
# or don't print at all(leave undef)
my $newhead_print = 1;#!!yes=1
my $newhead_fh = \*STDOUT;#alternative \*STDERR/another open fh
my $newhead_line = "#variant\talt_allele\tgen_hgvs\tprot_hgvs\tgene_sym\ttranscript\tgene_feature\n";


die "usage: gi_hgvs_break.pl file_of_trevors_output variant_id_delimiter(optional,\"|\")\n" unless @ARGV != 0;
$delim = $ARGV[1] if defined($ARGV[1]);#redefine with diff delim


my %var;#variants

open(HGVS,$ARGV[0]) || die "Cannot open input file of trevor's hgvs script output.\n";

<HGVS>;#skip header
#my $head = <HGVS>;#skip header
#print $head."\n";
while(<HGVS>){

	s/\n$//;#chomp gives lines diff colnums
	
	my @col=split(/\t/,$_);

	my $alt;#alt allele
	
	#parse gi hgvs script input format back to gcoords
	my $coord=$col[0];
	$coord=~s/-\d+//;
	if($coord =~ s/^(\w+):(\d+)(\D.*?)\/(\w+)$/\1$delim\2$delim\3/){
		$alt = $4;
	}
	else{
		die "Variant info did not parse correctly: ".$col[0]."\n";
	}

	
	#init new variant
	if(!defined($var{$coord})){
	
		#genesym,transid,exon/intron/etc.; add null value
		my @ref_null = map {if(/^$/){$_=$null_val}else{$_}} @col[1..3];
		my $ref = join("\t",@ref_null);
		
		$var{$coord} = {"ref",$ref,"alt",[],"cnomen",[],"pnomen",[]};
	}	
	
	push(@{$var{$coord}{"alt"}},$alt);
	push(@{$var{$coord}{"cnomen"}},$col[4]);
	push(@{$var{$coord}{"pnomen"}},$col[5]) if $col[5] ne "";
}
close(HGVS);


#print header (optional)
print $newhead_fh $newhead_line if $newhead_print;


#print out one position (one ref per line)
#if multi-allelic (multiple alt), reformats 
# each hgvs nomenclature into single entity
foreach my $loc (sort(keys(%var))){
	
	#alternate alleles
	my $alternates = join(",",@{$var{$loc}{"alt"}});
	
	my $cnom = form_nomen($var{$loc}{"cnomen"});
	my $pnom = form_nomen($var{$loc}{"pnomen"});
	$pnom = $null_val if $pnom eq "";#use null value if not coding
	
	print $loc."\t".$alternates."\t".$cnom."\t".$pnom."\t".$var{$loc}{"ref"}."\n";
}

exit;


sub form_nomen{
	#builds hgvs nomenclature 
	# for a given variant.  if array > 1, 
	# iterates through, removes both c. and p. 
	# from all elements and adds back in later.
	my $nomens = $_[0];#arr
	
	my $fin_nomen = $nomens->[0];#defaults to 1st (if only 1)
	
	if(@$nomens > 1){#multiallelic

		#strip nomens of their dots (c.,g.,p.)
		my $dottype;#c,g,p
		foreach my $nomen (@$nomens){
			$nomen =~ s/^([c,g,p])\.(.+)$/\2/;
			
			if(defined($dottype)){#inconsistent dot types
				warn "Nomenclature type inconsistent. ".$dottype." and ".$1."\n" if (defined($dottype) && $1 ne $dottype);
			}

			$dottype = $1;
		}
		
		$fin_nomen = $dottype.".[".join(";",@{$nomens})."]";
	}

	return $fin_nomen;
}

#my %var;while(<>){s/\n$//;my @col=split(/\t/,$_);my $coord=$col[0];$coord=~s/-\d+//;$coord=~s/^(\w+):(\d+)(\D.*?)\/\w+$/\1\|\2\|\3/;my @stuff=@col[2..4];$var{$coord}{"ref"}=\@stuff;$var{$coord}{"cnomen"}.=":::".$col[3];$var{$coord}{"pnomen"}.= ":::".$col[4];}foreach my $loc (sort(keys(%var))){my $cnom=$var{$loc}{"cnomen"};$cnom=~s/^::://;my $pnom=$var{$loc}{"pnomen"};$pnom=~s/^::://;print $loc."\t".$cnom."\t".$pnom."\t".join("\t",@{$var{$loc}{"ref"}})."\n";

#my %var;while(<>){s/\n$//;my @col=split(/\t/,$_);my $coord=$col[0];$coord=~s/-\d+//;$coord=~s/^(\w+):(\d+)(\D.*?)\/\w+$/\1\|\2\|\3/;my @stuff=@col[2..4];$var{$coord}{"ref"}=\@stuff;$var{$coord}{"cnomen"}.=":::".$col[3];$var{$coord}{"pnomen"}.= ":::".$col[4];}foreach my $loc (sort(keys(%var))){my $cnom=$var{$loc}{"cnomen"};$cnom=~s/^::://;my $pnom=$var{$loc}{"pnomen"};$pnom=~s/^::://;print $loc."\t".$cnom."\t".$pnom."\t".join("\t",@{$var{$loc}{"ref"}})."\n";}';
#perl -ne 'my @col=split(/\t/,$_);my @out;foreach my $column (@col[0..5]){if($column eq ""){push(@out,".");}else{push(@out,$column);}}print join("\t",@out);

#my %var;while(<>){s/\n$//;my @col=split(/\t/,$_);my $coord=$col[0];$coord=~s/-\d+//;$coord=~s/^(\w+):(\d+)(\D.*?)\/\w+$/\1\|\2\|\3/;my @stuff=@col[1..3];$var{$coord}{"ref"}=\@stuff;$var{$coord}{"cnomen"}.=":::".$col[4];$var{$coord}{"pnomen"}.= ":::".$col[5];}foreach my $loc (sort(keys(%var))){my $cnom=$var{$loc}{"cnomen"};$cnom=~s/^:+//;$cnom=~s/:::/\;/g;my $pnom=$var{$loc}{"pnomen"};$pnom=~s/^:+//;$pnom=~s/:::/\;/g;print $loc."\t".$cnom."\t".$pnom."\t".join("\t",@{$var{$loc}{"ref"}})."\n";}'  
# perl -ne 'my @col=split(/\t/,$_);my @out;foreach my $column (@col[0..5]){if($column eq ""){push(@out,".");}else{push(@out,$column);}}print join("\t",@out);' | perl -Mstrict -ne 'my @col=split(/\t/,$_);$col[1]=~s/\;[c,g]\./\;/g;$col[1]=~s/^([c,g]\.)/\1\[/;$col[1].="]" unless $col[1] eq ".";$col[2]=~s/\;p\./\;/g;$col[2]=~s/^p\./p\.\[/;$col[2].="]" unless $col[2] eq ".";print join("\t",@col);' > trevor.out.mergeable.tbl

