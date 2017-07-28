#!/usr/bin/env sh
#jje16, msl34 01192015
#vcf hack process same for clemens (classically), but for MuTect 
#outputted vcf instead of GATK's.
#does vcf merge, hgvs,
#output is a vcf expanded into a table, info name as header
set -e

#num seconds to wait be:1fore next step
SEC=180

##usage
if [ "$1" = "" ]; then
	echo "usage: vcf_mutect_tbl.sh run_directory_path"
	exit
fi


##dir with raw vcfs
DIR=$1



#rm weird chars
ls $DIR/*.vcf | \
 bsub_bldr.py -q pcpgmwgs -ep -o 'cat {} | clean_hidden.pl > {}.clean' | \
 bsub_bldr.py -q pcpgmwgs -ep -wp -o 'vcf_mutect_ordr.pl {}.clean > {}.clean.ordr' | \
 bsub_bldr.py -q pcpgmwgs -o -wp -ep 'vcf_mutect_nad.pl {}.clean.ordr > {}.clean.ordr.nad' | \
 bsub_bldr.py -q pcpgmwgs -wp -e -o 'vcf_rm_format.pl {}.clean.ordr.nad SS > {}.form.vcf' | \
 bsub_bldr_wait.py

# bsub_bldr.py -q pcpgmwgs -ep -wp -o 'vcf_rm_smpl.pl {}.clean.ordr.nad 9 > {}.clean.ordr.nad.nonorm' | \
# bsub_bldr.py -q pcpgmwgs -wp -e -o 'vcf_rm_format.pl {}.clean.ordr.nad.nonorm SS > {}.form.vcf' | \
# bsub_bldr_wait.py




##merge
#bgzip, tabix and vcf-merge
#from each plate dir, cp raw/*.clean.qd.fs.vcf to dir merge/prep
#not sure whether tabix needs "-h" to add header or no

#ls $DIR/*.form.vcf | perl -ne 'chomp;system("bgzip ".$_);'
#ls $DIR/*.form.vcf.gz | perl -ne 'chomp;system("tabix -h ".$_);'
#vcf-merge `ls $DIR/*.form.vcf.gz` > $DIR/all.merge.vcf

ls $DIR/*.form.vcf | bsub_bldr.py -q pcpgmwgs -o -ep 'bgzip {}' | \
 bsub_bldr.py -q pcpgmwgs -o -e -wp 'tabix -h {}.gz' | bsub_bldr_wait.py

vcf-merge `ls $DIR/*.form.vcf.gz` > $DIR/all.merge.vcf


##add hgvs nomenclature 
#rm chr or harmless if none
cat $DIR/all.merge.vcf | perl -ne 's/^chr//;print;' > $DIR/all.merge.nochr.vcf

vcf_to_gi_hgvs.sh $DIR/all.merge.nochr.vcf > $DIR/hgvs.tbl


###UNWANTED BY ASHLEY'S REQUEST
###zygosity
##zygos_bool.pl $DIR/all.merge.nochr.vcf > $DIR/merge_zygo.vcf


#make tag id/value pairs (GT=0/1:AD=4,13)
cat $DIR/all.merge.nochr.vcf | perl -ne 'if(/^\#/){print}else{s/\n$//;my @col=split(/\t/,$_);my $format=$col[8];my @form=split(/:/,$format);for(my $i=9;$i<@col;$i++){if($col[$i] ne "."){my @newval;my @val=split(/:/,$col[$i]);for(my $j=0;$j<@form;$j++){push(@newval,$form[$j]."=".$val[$j]);}$col[$i]=join(":",@newval);}}print join("\t",@col)."\n";}' > $DIR/keyval.vcf



##join merged vcf with hgvs tbl
#make common id (including header)
grep -v '^##' $DIR/keyval.vcf  | perl -ne 'my @arr=split(/\t/,$_);print $arr[0]."|".$arr[1]."|".$arr[3]."\t".$_;' | perl -ne 's/\#CHROM\|POS\|REF/\#variant/ if /\#C/;print' > $DIR/keyval_hgvsid.tbl


tbl_merge.pl $DIR/keyval_hgvsid.tbl $DIR/hgvs.tbl 5 | cut -f2,3,5,7-12,17- | perl -ne 'if(/^\#CHROM/){s/\#CHROM/chrom/;s/POS/pos/;s/REF/ref/;s/alt_allele/alt/;}print;' > $DIR/variant_final.txt

echo "File: variant_final.txt"
echo Done.

exit
