#!/usr/bin/env sh
set -e

#see summary comment below

#hard-coded values
GIUSER="lmm"
GIPASS="x377BLCi"

#temp files (rm after, filenames)
CLEANUP="true"
#CLEANUP="false"
TMPFILE1="tmp.gi.hgvs.script.tbl1"
TMPFILE2="tmp.gi.hgvs.script.tbl2"


###summary: get hgvs nomenclature 
# for all variants in a vcf
# from geneinsight
#prints stdout tab delimited
#	chromosome|position|refallele
#	alternate allele
#	genesym
#	transcriptid
#	exon/intron/ect.
#	gene nomen
#	pnomen<nl>

#usage
if [ "$1" = "" ]; then
	echo "usage: vcf_to_gi_hgvs.sh vcf_to_query rm_temp_files(optional,default true)"
	exit 1
fi

VCF=$1

#2nd arg to indicate rm temp files (true/false)
if [ "$2" != "" ]; then
	CLEANUP=$2
fi

##steps
#convert from vcf to input format for trevor's script
gi_hgvs_form.pl $VCF > $TMPFILE1

#run trevors script
coords2lmmcds.py -l $GIUSER -p $GIPASS $TMPFILE1 > $TMPFILE2

#join back variants by pos and ref allele as output
gi_hgvs_reform.pl $TMPFILE2 $DELIM

if $CLEANUP; then
	rm $TMPFILE1
	rm $TMPFILE2
fi

exit 0
