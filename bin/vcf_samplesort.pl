#!/usr/bin/env perl
use strict;

#substitute a vcf sample column 
# having a gatk predicted zygosity 
# with zy=het/zy=hom.
#for research core amplicon seq 


#cat merge/all.vcf | grep -v '^#' | perl -Mstrict -ne 'if(/^\#/){print;}else{chomp;my @col=split(/\t/,$_);my @newcol=@col[0..8];my $zy;for(my $i=9;$i<@col;$i++){if($col[$i]=~/^(\d\/\d):/){$zy="zy=het";$zy="zy=hom" if $1 eq "0/0";}elsif($col[$i] eq "."){$zy=".";}else{$zy=$col[$i];warn "sample column niether a predicted zygosity or a dot! column: ".$i.", value: ".$col[$i]."..using original value\n";}push(@newcol,$zy);}print join("\t",@newcol)."\n";}'

die "usage: zygos_bool.pl merged_samples.vcf\n" unless @ARGV==1;

open(VCF,$ARGV[0]) || die "Cannot open VCF file: ".$ARGV[0]."\n";
while(<VCF>){
	if(/^\#/){
		print;
	}
	else{
		chomp;
		my @col=split(/\t/,$_);
		
		my @newcol=@col[0..8];
		my $zy;
		
		for(my $i=9;$i<@col;$i++){#sample cols
			
			if($col[$i]=~/^(\d\/\d):/){#predicted zygosity
				print $1."\tone\n";
				if($1 eq "0/0"){
					#print $1."\twhoa\n";
					$zy="zy=hom";
				}
				else{
					$zy="zy=het";
				}
			}
			elsif($col[$i] eq "."){
			
				$zy=".";
			}
			else{
			
				warn "sample column niether a predicted zygosity or a dot! chrom: ".$col[0].", pos: ".$col[1].", column: ".$i.", value: ".$col[$i]."..using original value\n";
				$zy=$col[$i];
			}
			
			push(@newcol,$zy);
		}
		
		#print join("\t",@newcol)."\n";
	}

}
close(VCF);

exit;
