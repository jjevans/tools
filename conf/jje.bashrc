# jje, .bashrc
#updated 02282014
#updated 04252014
#updated 11052014


##project navigation
#export RUN=/scratch/pcpgm/jje/projects/evaluate/dbsnfp/run/run_10312014/snpsift_11032014
#alias run="cd $RUN"
#alias 1a="cd $RUN/1A"
#alias 2a="cd $RUN/2A"
#alias 3a="cd $RUN/3A"



# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

####important info
#gi user/pass lmm/x377BLCi
####

######ENV######
##basics
export EDITOR=vi
export PS1='\[\e[0;34m\][\[\e[1;34m\]\D{%D}:\[\e[0;34m\]\h//\W \[\e[0;32m\]\!\[\e[0;34m\]]:\[\e[m\] '
#export PS1='\[\e[0;31m\][\D{%a %D}:\W \!]:\[\e[m\] '
#export PS1="[\h:\W \!]: "
export DISPLAY=:0.0

##misc
export ALAOPT='--alltrans --nonnsplice --nomispred --outputannonly'

##locations
#external
export NCBIFTP=ftp.ncbi.nlm.nih.gov

#internal
export DATA=/data/pcpgm
export SCRATCH=/scratch/pcpgm
export SHARE=$SCRATCH/share

#personal dirs
export JJEDATA=$DATA/jje
#export VAL=$JJEDATA/validation/jje16

#biofx validation
export VALID=/data/pcpgm/validation/jje16

export JJESCRATCH=$SCRATCH/jje
export PROJ=$JJESCRATCH/projects
export AMPL=$PROJ/ampl_seq/gba_snca0
export VCF=$AMPL/vcf_hack
export COV=$AMPL/coverage

#wgs
export WGS=$DATA/wgs
export WGS_PROC=$WGS/wgs_processing
#export WGS_BIN=$WGS/enrichment
#export WGS_ANNO=$WGS/enrichment/WGS_Annotation_Operation

#exome anno
export ANNOWGS=/PHShome/jje16/Tools/internal/SVN/wgs/branches/annotation-dev-et85

##my scripts
export MINE=$HOME/Tools/me/bin

##svn
export SVN=$HOME/Tools/internal/SVN
export ME=$SVN/ngs/bioinfo/People/Jason

##instances
#export GAL=/data/pcpgm/galaxy-pcpgm/galaxy-dist
#export JB=/data/pcpgm/jje/Tools/JBrowse-1.7.6

##data and databases
export HG19ME=/data/pcpgm/jje/data/seq/ref/hg19/hg19.fa
export HG19=/scratch/pcpgm/share/reference/hg19/Homo_sapiens_assembly19.fasta

export NSFPDIR=/scratch/pcpgm/share/annot_db/dbnsfp/versions/v2.7
#export NSFPRAW=$NSFPDIR/raw
export NSFP=$NSFPDIR/raw/dl_merged/dbNSFP2.7.txt.gz


#dbs
export MYSQL_HOME=${HOME}/db/mysql_install/mysql_5.6.1
#possibly need ORACLE_HOME or LD_LIBRARY_PATH or whatever to get oracle going
export LD_LIBRARY_PATH=/scratch/pcpgm/share/software/oracle/11.2/client64/lib:$LD_LIBRARY_PATH

##software
export PICARD=$JJEDATA/tools/align/picard/current
export GATK=$JJEDATA/tools/variant/gatk/current/GenomeAnalysisTKLite.jar

#snpeff
export SNPEFFDIR=$SHARE/software/snpEff
#export SNPEFFDIR=$SHARE/software/snpEff_v3_6
export SIFT=$SNPEFFDIR/SnpSift.jar
export SNPEFF=$SNPEFFDIR/snpEff.jar


#LSF libs
#export DRMAA_LIBRARY_PATH=${HOME}/.local/lib/python2.7/site-packages/drmaa-0.5-py2.7.egg
#export DRMAA_LIBRARY_PATH=${HOME}/build/DRMAA/lib/libdrmaa.so
#export DRMAA_LIBRARY_PATH=${HOME}/build/lsf_drmaa-1.0.3/lib/libdrmaa.so
export DRMAA_LIBRARY_PATH=/scratch/pcpgm/share/local/lib/libdrmaa.so


##modules
if [ -n "$MODULESHOME" ]; then

	#group
	alias mod_grp="\
		module use /apps/modulefiles/lab/ppm; module load snpeff/default bcl2fastq/default"

	#programming
	alias mod_prog="\
		module load BioPerl-1.6.901 perl/default python/2.7.5 R/R-3.0.0 vim/default"
	
	#seq and aln
	#use ver on share#module load bwa-0.6.2
	alias mod_seq="\
	    module load casava-1.8.2 fastx_toolkit-0.0.13 blatSrc35 novoalign/novoalign_v3-1.00.02 cufflinks/default mummer3.23 ncbi-blast-2.2.26 tophat/2.0.10 cufflinks/2.2.1 bowtie2/2.1.0 cummeRbund-1.2.0"

	#txt
	module load bedtools
	module load vcftools/default
	module load samtools/default
	module load tabix/default

	#variant
	alias mod_var="\
	module load gatk-2.2.4 picard-tools-1.8.4"

	#num crunch
	alias mod_num="\
	module load numpy/1.7.2 scipy/default"

	#sys
	alias mod_sys="\
	module load gcc/default zlib/1.2.8"

fi



##paths
export PATH=/PHShome/jje16/Tools/me/bin:$ME/bin:${HOME}/Tools/internal/bin:/scratch/pcpgm/share/software/current/bin:/PHShome/jje16/.local/bin:$SVN/ngs/variant-reporting/annotation/trunk:/PHShome/jje16/build/gvcftools-0.16/bin:$PATH
#fix these directories below but add to PATH for now!!!
export PATH=$PATH:${HOME}/build/bedtools2-2.19.1/bin:${HOME}/build/vcftools_0.1.12a/bin:${HOME}/build/tabix-0.2.6:/PHShome/jje16/db/mysql_install/mysql_5.6.1/bin:$JJEDATA/tools/align/e-PCR_dir/Linux-x86_64:${JJEDATA}/tools/align/mummer_dir/MUMmer3.23

export PERL5LIB=$ME/lib:$SHARE/software/lib:${PERL5LIB}

export PYTHONPATH=${HOME}/Tools/internal/SVN/ngs/bioinfo/People/Jason/lib:${HOME}/Tools/internal/SVN/ngs/NVA/trunk/modules:${HOME}/.local/lib/python2.7/site-packages:/scratch/pcpgm/share/lib/python2.7/site-packages:/usr/lib/python2.6/site-packages:${PYTHONPATH}

export CLASSPATH=/scratch/pcpgm/share/software/current/java:$SNPEFFDIR:$CLASSPATH


##aliases
#file mods
alias rc='vi ~/.bashrc'
alias src='source ~/.bashrc'
alias useful='cat >> ~/useful_cmds.txt'

#hack
alias strictn='perl -Mstrict -ne '
alias stricte='perl -Mstrict -e '

#bioinfo
alias picard='ls $PICARD'
alias gatk='java -Xms4g -Xmx24g -jar $GATK'
alias snpeff='java -Xms4g -Xmx24g -jar $SNPEFF'
alias sift='java -Xms4g -Xmx24g -jar $SIFT'

#lsf: interactive
alias live="bsub -q pcpgmwgs -R 'rusage[mem=16000]' -n 1 -Is bash"
alias liveX="bsub -q pcpgmwgs -R 'rusage[mem=16000]' -XF -n 1 -Is bash"
alias high="bsub -q pcpgmwgs -R 'rusage[mem=32000]' -n 1 -Is bash"
alias highX="bsub -q pcpgmwgs -R 'rusage[mem=32000]' -XF -n 1 -Is bash"
alias alive="bsub -q pcpgmwgs -m pcpgmwgs_hg -R 'rusage[mem=16000]' -n 1 -Is bash"
alias aliveX="bsub -q pcpgmwgs -m pcpgmwgs_hg -R 'rusage[mem=16000]' -XF -n 1 -Is bash"
alias olive="bsub -q pcpgmwgs -m pcpgmtest_hg -R 'rusage[mem=16000]' -n 1 -Is bash"
alias oliveX="bsub -q pcpgmwgs -m pcpgmtest_hg -R 'rusage[mem=16000]' -XF -n 1 -Is bash"

alias clinic='bsub -q pcpgm -n 1 -Is bash'
alias clinicX='bsub -q pcpgm -XF -n 1 -Is bash'

alias bsubwgs='bsub -q pcpgmwgs -m pcpgmwgs_hg'
alias bsubtest='bsub -q pcpgmwgs -m pcpgmtest_hg'

#multi-core
alias dual="bsub -q pcpgmwgs -m pcpgmwgs_hg -R 'rusage[mem=24000,ncpus=2] span[hosts=1]' -n 2 -o lsf.out -e lsf.err"
alias dualwgs="bsub -q pcpgmwgs -R 'rusage[mem=24000,ncpus=2] span[hosts=1]' -n 2 -o lsf.out -e lsf.err"

alias multi="bsub -q pcpgmwgs -m pcpgmwgs_hg -R 'rusage[mem=32000,ncpus=4] span[hosts=1]' -n 4 -o lsf.out -e lsf.err"
alias multiwgs="bsub -q pcpgmwgs -R 'rusage[mem=32000,ncpus=4] span[hosts=1]' -n 4 -o lsf.out -e lsf.err"

alias oct="bsub -q pcpgmwgs -m pcpgmwgs_hg -R 'rusage[mem=48000,ncpus=8] span[hosts=1]' -n 8 -o lsf.out -e lsf.err"
alias octwgs="bsub -q pcpgmwgs -R 'rusage[mem=48000,ncpus=8] span[hosts=1]' -n 8 -o lsf.out -e lsf.err"

alias super="bsub -q pcpgmwgs -m pcpgmwgs_hg -R 'rusage[mem=96000,ncpus=16] span[hosts=1]' -n 16"

#places
#external
alias ncbi='ftp $NCBIFTP'

#internal
alias alamutvm='ssh alamut-ht1.dipr.partners.org'
alias ppm='ssh ppm.dipr.partners.org'
alias pcpgm='ssh pcpgm.dipr.partners.org'
alias pdp='ssh primerapp-new.dipr.partners.org'
alias pdpdev='ssh pdp-dev.dipr.partners.org'
alias share='cd $SHARE'

#people
alias wgstest='sudo -u pcpgmwgs_test bash'
alias wgsprod='sudo -u pcpgmwgs_prod bash'

#mysql
alias mysqlstop='${MYSQL_HOME}/bin/mysqladmin --socket=/PHShome/jje16/db/mysql_install/mysql_5.6.1/mysql.sock  shutdown'
alias mysqlstart='${MYSQL_HOME}/bin/mysqld --socket=/PHShome/jje16/db/mysql_install/mysql_5.6.1/mysql.sock &'
alias mysqlsock='${MYSQL_HOME}/bin/mysql --socket=/PHShome/jje16/db/mysql_install/mysql_5.6.1/mysql.sock'
alias mysqlreset='mysqlstop;mysqlstart'

#reminders
alias err="echo 2\&\>1"

#misc
alias os='cat /etc/issue'
alias go='mkdir_and_cd.pl'

#commands
#ls
alias lrt='ls -lrt'
alias lscolor='ls --color'
alias lsall='ls -a'
alias lshuman='ls -h'
alias lsrecur='ls -R'
alias lsgrp='ls --group-directories-first -lut'

#history
alias h=history
alias hh="history | tail -500"

#du
alias duh='du -h'
alias dual='du -a'
alias dudepth='du --max-depth=2'

#grep
alias g='grep'
alias gv='grep -v'
alias gn='grep -n'
alias gct='grep -c'

#java
alias javadef='java -Xms4g -Xmx8g'
alias javaj='java -Xms4g -Xmx32g -jar'

#utilities
alias bun='bunzip2'
alias m=more
alias w=which

