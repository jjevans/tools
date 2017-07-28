#!/usr/bin/env sh
set -e

if [ "$1" == "" ]; then
	echo usage: vcf_research_tbl.sh dir_of_vcf_with_extension .vcf
	exit
fi

SLEEPYTIME=60
OUTPUT=vcf.tbl
RUNDIR=`date '+run.%m-%d-%y-%H-%M-%S-%N'`

echo NOTICE: create and change dir to $RUNDIR

mkdir $RUNDIR
#mkdir $RUNDIR/raw

for arg in $@
do
	cp $arg $RUNDIR
done

cd $RUNDIR
#mkdir addinfo
#mkdir final
#mkdir merge_vcf


##clean hidden chars
ls *.vcf | perl -ne 'chomp;my $out=$_.".clean.vcf";my $cmd="bsub -q pcpgmwgs -n 1 -R \"rusage[mem=4000]\" -o out.out -e err.err \"cat $_ \| clean_hidden.pl \| stdin_to_file.pl $out\"";print $cmd."\n";system($cmd)'

echo sleepytime: $SLEEPYTIME
sleep $SLEEPYTIME

##info to sample fields
#add qd to sample col
ls *.clean.vcf | perl -ne 'chomp;my $out=$_.".qd";my $cmd="bsub -q pcpgmwgs -n 1 -R \"rusage[mem=4000]\" -o out.out -e err.err \"vcf_info_to_format.pl $_ QD \| stdin_to_file.pl $out\"";print $cmd."\n";system($cmd)'

echo sleepytime: $SLEEPYTIME
sleep $SLEEPYTIME

#add fs to sample col
ls *.qd | perl -ne 'chomp;my $out=$_.".fs.vcf";my $cmd="bsub -q pcpgmwgs -n 1 -R \"rusage[mem=4000]\" -o out.out -e err.err \"vcf_info_to_format.pl $_ FS \| stdin_to_file.pl $out\"";print $cmd."\n";system($cmd)'

echo sleepytime: $SLEEPYTIME
sleep $SLEEPYTIME
echo NO MORE SLEEP.

##vcf-merge all samples
ls *.qd.fs.vcf | perl -ne 'chomp;system("bgzip ".$_);'
ls *.qd.fs.vcf.gz | perl -ne 'chomp;system("tabix -h ".$_);'

vcf-merge `ls *.qd.fs.vcf.gz` > all.merge.vcf



##hgvs
#uses dir "addinfo"
#rm chr
cat all.merge.vcf | perl -ne 's/^chr//;print;' > all.merge.nochr.vcf

vcf_to_gi_hgvs.sh all.merge.nochr.vcf > hgvs.tbl


##zygosity
zygos_bool.pl all.merge.nochr.vcf > merge_zygo.vcf


##keyval pair tag to value
cat merge_zygo.vcf | perl -ne 'if(/^\#/){print}else{s/\n$//;my @col=split(/\t/,$_);my $format=$col[8];my @form=split(/:/,$format);for(my $i=9;$i<@col;$i++){if($col[$i] ne "."){my @newval;my @val=split(/:/,$col[$i]);for(my $j=0;$j<@form;$j++){push(@newval,$form[$j]."=".$val[$j]);}$col[$i]=join(":",@newval);}}print join("\t",@col)."\n";}' > keyval.vcf



##merge zygosity, hgvs,
#uses dir "final"
grep -v '^##' keyval.vcf  | perl -ne 'my @arr=split(/\t/,$_);print $arr[0]."|".$arr[1]."|".$arr[3]."\t".$_;' | perl -ne 's/\#CHROM\|POS\|REF/\#variant/ if /\#C/;print' > zygo_hgvsid.tbl


#tbl_merge.pl zygo_hgvsid.tbl addinfo/hgvs.tbl 5 | cut -f2,3,5,7-12,17- | perl -ne 'if(/^\#CHROM/){s/\#CHROM/chrom/;s/POS/pos/;s/REF/ref/;s/alt_allele/alt/;}print;' > $OUTPUT

#this cmd works, but columns vary based on num samples in merged vcf
#tbl_merge.pl zygo_hgvsid.tbl hgvs.tbl | perl -ne 's/\n$//;my @col=split(/\t/,$_);print join("\t",@col[1..5])."\t".join("\t",@col[26..30])."\t".join("\t",@col[10..24])."\n";' | perl -ne 's/\#CHROM\tPOS\tID\tREF\tALT/chrom\tpos\tid\tref\talt/;print;' > vcf.tbl

echo DONE: $OUTPUT
exit




