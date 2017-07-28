#!/usr/bin/env sh
set -e


#see below for desc, either DOALL=1 processes whole process, otherwise use DO var for each section
DOALL=1
#or
DOFORMAT1=0
DOMERGE=0
DOHGVS=1
DOFORMAT2=1
DOTBL=1

DOZY=0 #independent of DOALL
DOWARN=1
DOCLEAN=0


####
#merge directory of multiple vcfs to one single table with 
# their hgvs nomenclature and each sample's values 
# in sample column
#jje16, msl34	01192015
#personalized medicine bioinformatics

#vcf hack process for clemens (classically) vcf merge, hgvs,
#output is a vcf expanded into a table, info name as header, 
# with option to added sample field ZY=het/hom interpreted from gatk GT
#final output file named default or optionally provided as arg 2
#creates many intermediate files in the directory provided
####

#final table filename default
FILENAME=variant_final.txt


#process is split into 5 parts making 5 checkpoints to enter process.  
#value of 1 enables that part
#parts: 
#	initial conversion, parse, format of input vcfs
#	merging man vcfs into one
#	get hgvs nomenclature
#	subsequent conversion, format of merged vcf including zygosity ZY=HET 
#	final table merge into final output file

#checkpoint system of being able perform some or all of 5 parts of this process independently
#variables indicating parts to enter and skip
#if DOALL=1 (set at top), all steps are run regardless of individual DO variable 
# for each section (DOALL trumps all)
#NOTE: zygosity interpretation (ZY=HOM) with DO var called DOZY 
# must be set explicitly (DOALL doesn't affectit)

#override each parts DO variable if DOALL is 1
#NOTE: zygosity part (DOZY) needs value of 1 set explicitly, DOALL doesn't affect DOZY
#if DOALL=1, sets all steps to 1 and run all parts
if [ "$DOALL" == 1 ]; then
	DOFORMAT1=1
	DOMERGE=1
	DOHGVS=1
	DOFORMAT2=1
	DOTBL=1
fi

#DOWARN checks and warns if final output file does not exist or is zero-sized
#DOCLEAN !unimplemented! removes the unneeded intermediate files produced


##usage
#arg 1: dir to find vcfs
if [ "$1" = "" ]; then
	echo "usage: vcf_clemens.sh run_directory_path output_file (optional, default $FILENAME)" >&2
	exit
else
	DIR=$1
fi

#arg 2 (optional): final output table filename
if [ "$2" != "" ]; then
	FILENAME=$2
fi

#final output file
FILEFINAL=$DIR/$FILENAME

# key files used to chain optional parts together
#filename suffix for all files after conversion I but before merge
#FILESUFFIX=fs.tomrg.vcf
FILESUFFIX=tomerge.vcf
FILEMERGE=$DIR/all.merge.vcf
FILEZY=$DIR/merge_zygo.vcf
FILEHGVS=$DIR/all.hgvs.tbl
FILEFORMAT2=$DIR/keyval.vcf

#keep track of last vcf processed and use that file even when skip section
PROCVCF=$FILEMERGE #defaults to first vcf produced from merge


##error trap function
raise () {
	# exception trap, echo error message and exit
	echo ":::!!! error: trapped exception in at line $1, script $0" >&2
	exit
}
trap 'raise $LINENO' ERR


echo processing. >&2

##conversion and format part 1
#clean hidden chars, add qd, fs from info to sample col
#all clean, formtoinfo qd, formtoinfo fs in one command
#uses bsub to submit jobs for multiple vcfs and waits to finish 
# before proceeding to next step
#commented out this method to sleep while waiting for bsub jobs to finish
# to use cleaner method below using bsub_bldr
if [ "$DOFORMAT1" == 1 ]; then
	echo "::: start conversion I" >&2

	#die if no .vcf files in dir
	NUM=`ls $DIR/*.vcf 2>/dev/null | wc -l`
	if [ "$NUM" == 0 ]; then
		echo ":::!!! error: no files exist with suffix *.vcf at line $LINENO" >&2
		exit
	fi
	unset NUM


	#submits and waits for all jobs on lsf using bsub_bldr and bsub_bldr_wait
	#rm hidden funny chars (found a lot in myseq vcfs) 
	# and remove chr from chromosome name if present
	ls $DIR/*.vcf | bsub_bldr.py -e -q pcpgmwgs -R 4000 -o 'cat {} | clean_hidden.pl | perl -ne "s/^chr//;print;" > {}.clean' | bsub_bldr_wait.py

	ls $DIR/*.clean | bsub_bldr.py -e -q pcpgmwgs -R 4000 -o "vcf_info_to_format.pl {} QD > {}.qd" | bsub_bldr_wait.py

	ls $DIR/*.qd | bsub_bldr.py -e -q pcpgmwgs -R 4000 -o "vcf_info_to_format.pl {} FS > {}.$FILESUFFIX" | bsub_bldr_wait.py


	echo "::: file conversion I filename suffix: $FILESUFFIX" >&2
	echo "::: done conversion I" >&2

else echo "::: skip conversion I" >&2 
fi


##vcf merge
#bgzip, tabix index and vcf-merge
if [ "$DOMERGE" == 1 ]; then
	echo "::: start vcf merge" >&2

	#die if no files to merge
	#gets number of files ending in both FILESUFFIX and 
	# FILESUFFIX.gz (if already bgzipped)
	NUM=`ls $DIR/*.$FILESUFFIX 2>/dev/null | wc -l`
	ZIPS=`ls $DIR/*.$FILESUFFIX.gz 2>/dev/null | wc -l`
	
	#bgzip if not already
	if [ "$NUM" != 0 ]; then
		echo "::: running bgzip for merge" >&2
	
		ls $DIR/*.$FILESUFFIX | bsub_bldr.py -e -q pcpgmwgs -o 'bgzip {}' | bsub_bldr_wait.py
	
	elif [ "$ZIPS" != 0 ]; then
		 echo "::: vcf files to merge already bgzipped, skipping" >&2
	else
		echo ":::!!! error: no files exist with filename suffix $FILESUFFIX (nor .gz) at line number $LINENO" >&2
		exit
	fi

	unset NUM
	unset ZIPS


	#tabix index
	ls $DIR/*.$FILESUFFIX.gz | bsub_bldr.py -e -q pcpgmwgs -o 'tabix -h {}' | bsub_bldr_wait.py

	#merge all vcfs
	vcf-merge `ls $DIR/*.$FILESUFFIX.gz` > $FILEMERGE

	#track most recently created vcf what parts are run
	PROCVCF=$FILEMERGE
	
	echo "::: file merged to single vcf: $FILEMERGE" >&2 
	echo "::: done vcf merge" >&2 

else echo "::: skip vcf merge" >&2 
fi


##hgvs
if [ "$DOHGVS" == 1 ]; then
	echo "::: start hgvs assignment" >&2

	#die if required files don't exist
	#needs to have vcf to use for next part.
	#requires PROCVCF defined earlier in the process or 
	# existing file defined above in var FILEMERGE
	if [ ! -f "$PROCVCF" ]; then
		echo ":::!!! error: no vcf file found at line $LINENO, $PROCVCF" >&2
		exit
	fi
		
	#query gi for hgvs nomenclature
	vcf_to_gi_hgvs.sh $PROCVCF > $FILEHGVS

	echo "::: file hgvs: $FILEHGVS" >&2 
	echo "::: done hgvs assignment" >&2 

else echo "::: skip hgvs" >&2  
fi


##translate zygosity (ZY=HET OR ZY=HOM) from gatk GT field
# Note: not confident this accounts for all GT cases
if [ "$DOZY" == 1 ]; then
	echo "::: start zygosity 'ZY' field insertion" >&2

	#die if required files don't exist
	if [ ! -f "$PROCVCF" ]; then
		echo ":::!!! error: no vcf file found at line $LINENO, $PROCVCF" >&2
		exit
	fi

	zygos_bool.pl $PROCVCF > $FILEZY
	
	PROCVCF=$FILEZY

	echo "::: file zygosity field insertion: $FILEZY" >&2
	echo "::: done zygosity 'ZY' field insertion" >&2

else echo "::: skip zygosity" >&2
fi


##formatting and conversion making key value pairs of 
# FORMAT ids and sample vals (so sample value 0/1 now is GT=0/1)
if [ "$DOFORMAT2" == 1 ]; then
	echo "::: start conversion II" >&2

	#die if required files don't exist
	if [ ! -f "$PROCVCF" ]; then
		echo ":::!!! error: no vcf file found at line $LINENO, $PROCVCF" >&2
		exit
	fi
	
	#from INFO fields make each sample have keyval pairs of 
	# INFO id and value (id=value, ex GT=0/1)
	# merges id in FORMAT col to vals in sample columns in order

	cat $PROCVCF | vcf_keyval.pl > $FILEFORMAT2

	PROCVCF=$FILEFORMAT2

	echo "::: file conversion II: $FILEFORMAT2" >&2
	echo "::: done conversion II" >&2

else echo "::: skip conversion II" >&2
fi


##merge hgvs table and vcf
#combine hgvs table and last VCF processed whether vcf produced by merge or zygosity sections

#make common id (including header)
#remove vcf header, reformat chr, pos, ref, alt 
# to id in first col to merge (12|20000000|A|C)
#actual merge of table (from vcf) and hgvs nomen table from gi
#cut out interesting columns (remove previously unwanted vcf columns)
if [ "$DOTBL" == 1 ]; then
	echo "::: start table merge" >&2

	#die if required files don't exist
	if [ ! -f "$PROCVCF" ]; then
		echo ":::!!! error: no vcf file found at line $LINENO, $PROCVCF" >&2
		exit

	elif [ ! -f "$FILEHGVS" ]; then
		echo ":::!!! error: no hgvs table exists at line $LINENO, $FILEHGVS" >&2
		exit
	fi


	#make unique id in first column for intermediate file to merge
	# uniq id: chr|pos|start|end
	KEYVAL=$DIR/keyval_hgvsid.tbl
	
	TBLUNIQ=$FILEHGVS.uniq.tbl
	
	grep -v '^##' $PROCVCF  | tbl_mkid.pl 0,1,3 > $TBLUNIQ
		
	cat $TBLUNIQ | perl -ne 's/\#CHROM\|POS\|REF/\#variant/ if /\#C/;print'	> $KEYVAL

		
	#final merge of vcf and hgvs table 
	FILEWHOLE=$KEYVAL.all.tbl
	
	tbl_merge.pl $KEYVAL $FILEHGVS 5 > $FILEWHOLE
	
	#chop out cols and prettify the header values
	cat $FILEWHOLE | cut -f2,3,5,7-12,17- | perl -ne 'if(s/\#CHROM/chrom/){ s/POS/pos/; s/REF/ref/; s/alt_allele/alt/; } print;' > $FILEFINAL
	
	echo "::: file table merge: $FILEFINAL" >&2 
	echo "::: done table merge" >&2 	

else echo "::: skip table merge" >&2 
fi


##final output file checks and warning (exists, non-zero check)
# if option to warn and did final table merge
if [ "$DOWARN" == 1 ] && [ ! -s "$FILEFINAL" ]; then
	echo ":::!!! warning: final file not found or zero-sized, $FILEFINAL" >&2
fi

echo "::: done." >&2

exit

