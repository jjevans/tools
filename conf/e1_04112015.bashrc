# jje, .bashrc
#updated 02282014
#updated 04252014
#updated 11052014

module load intel_parallel_xe/xe
module load R-mkl/3.0.2


##project navigation
#export RUN=/scratch/pcpgm/jje16/projects/evaluate/dbsnfp/run/run_10312014/snpsift_11032014
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
#gigpad asap/b1uekar5
####

#biofx usernames
alias peeps="perl -e 'print \"et85\nmsl34\nrs433\njje16\nplr1\ncg615\nhs747\n\"'"

######ENV######
##basics
export EDITOR=vi
export PS1='\[\e[0;34m\][\[\e[1;34m\]\D{%D}:\[\e[0;34m\]\h//\W \[\e[0;32m\]\!\[\e[0;34m\]]:\[\e[m\] '
#export PS1='\[\e[0;31m\][\D{%a %D}:\W \!]:\[\e[m\] '
#export PS1="[\h:\W \!]: "
export DISPLAY=:0.0

##misc
export PHRED_PARAMETER_FILE=/scratch/pcpgm/share/etc/washu/phredpar.dat
export ALAOPT='--alltrans --nonnsplice --nomispred --outputannonly'

##locations
#external
export NCBIFTP=ftp.ncbi.nlm.nih.gov

#internal
export DATA=/data/pcpgm
export SCRATCH=/scratch/pcpgm
export SHR=$SCRATCH/share
export SHRBIN=$SHR/bin
export SHRPY=$SHR/lib/python2.7
export SHRPL=$SHR/lib/perl5

#data
export SLXA=$DATA/solexa/solexa_runs
alias solexa='cd $SLXA'

#personal dirs
export JJEDATA=$DATA/jje16
#export VAL=$JJEDATA/validation/jje16

#projects
export VIS=/scratch/pcpgm/jje16/projects/viscap/
export VBIN=$VIS/bin
export VRUN=$VBIN/VisCap_asap.R

#biofx validation
export VALID=/data/pcpgm/validation/jje16

export JJESCRATCH=$SCRATCH/jje16
export PROJ=$JJESCRATCH/projects
export AMPL=$PROJ/ampl_seq

#asap
export ASAP=$DATA/asap-dev-jje16
alias asap='cd $ASAP'
export ABIN=$ASAP/bin
alias bin='cd $ABIN'
export APERL=$ASAP/lib/perl
alias ape='cd $APERL'
export APY=$ASAP/lib/python
alias apy='cd $APY'
export WRK=$ASAP/work
alias work='cd $WRK'
export PST=$ASAP/post
alias post='cd $PST'
export SAND=/data/pcpgm/jje16/asap-sandbox-jje16
alias sand='cd $SAND'
#wgs
export WGS=$DATA/wgs
export WGS_PROC=$WGS/wgs_processing
#export WGS_BIN=$WGS/enrichment
#export WGS_ANNO=$WGS/enrichment/WGS_Annotation_Operation

#projects
# exome anno
export ANNOWGS=/PHShome/jje16/Tools/internal/SVN/wgs/branches/annotation-dev-et85

##my scripts
export MINE=$HOME/Tools/me/bin

##svn
export SVN=$HOME/Tools/internal/SVN
export ME=$SVN/ngs/bioinfo/People/Jason
export BFX=$SVN/ngs/bioinfo/Projects

#projects
export NVA=$SVN/NVA/trunk
export NVAMOD=$NVA/modules

##instances

##data and databases
export HG19ME=/data/pcpgm/jje16/data/seq/ref/hg19/hg19.fa
export HG19=/scratch/pcpgm/share/reference/hg19/Homo_sapiens_assembly19.fasta

export NSFPDIR=/scratch/pcpgm/share/annot_db/dbnsfp/versions/v2.7
#export NSFPRAW=$NSFPDIR/raw
export NSFP=$NSFPDIR/raw/dl_merged/dbNSFP2.7.txt.gz


#dbs
export MYSQL_HOME=${HOME}/db/mysql_install/mysql_5.6.1
#possibly need ORACLE_HOME or LD_LIBRARY_PATH or whatever to get oracle going
export LD_LIBRARY_PATH=/scratch/pcpgm/share/software/oracle/11.2/client64/lib:$LD_LIBRARY_PATH
export TNS_ADMIN=/scratch/pcpgm/share/db/ora

##software
export PICARD=$SHR/software/picard/picard-tools-1.79
export GATK=$SHR/software/gatk_dir/gatk_3.1-1/GenomeAnalysisTK.jar
export PY279=/scratch/pcpgm/share/software/py/2.7.9

#snpeff
export SNPEFFDIR=$SHR/software/snpEff
export SIFT=$SNPEFFDIR/SnpSift.jar
export SNPEFF=$SNPEFFDIR/snpEff.jar


#libs
export DRMAA_LIBRARY_PATH=/scratch/pcpgm/share/local/lib/libdrmaa.so


##modules
if [ -n "$MODULESHOME" ]; then

	#group
	module use /apps/modulefiles/lab/ppm
	alias biofx='module load biofx'
	alias nobiofx='module unload biofx'

	#langs and environ
	#module load R/3.1.1-asap

	#tools
	module load bedtools/default
	module load vcftools/default
	module load samtools/default

	#sys
	module load gcc/default 
	#zlib/1.2.8
	module load boost-1.38.0
	#module load cmake/default
fi



##paths
export PATH=/scratch/pcpgm/share/software/current/bin:$HOME/Tools/me/bin:$ME/bin:$HOME/Tools/internal/bin:$SHRBIN:$SHRCURRBIN:$ABIN:$PY279/bin:$NVA:$PATH

export PERL5LIB=$ME/lib:$SHRCURRLIB:$SHRPL:$APERL:$PERL5LIB
export PYTHONPATH=$ME/lib:$SHRPY:$SHRPY/site-packages:$APY:$NVAMOD:$PYTHONPATH
#export CLASSPATH=/scratch/pcpgm/share/software/current/java:$SNPEFFDIR:$CLASSPATH


##aliases
#file mods
alias rc='vi ~/.bashrc'
alias src='source ~/.bashrc'
alias useful='cat >> ~/useful_cmds.txt'
alias cmds='cat ~/useful_cmds.txt'

#hack
alias strictn='perl -Mstrict -ne '
alias stricte='perl -Mstrict -e '

#bioinfo
alias picard='ls $PICARD'
alias gatk='java -Xms4g -Xmx12g -jar $GATK'
alias snpeff='java -Xms4g -Xmx24g -jar $SNPEFF'
alias sift='java -Xms4g -Xmx24g -jar $SIFT'

#lsf: interactive
alias live="bsub -q pcpgmwgs -R 'rusage[mem=16000]' -n 1 -Is bash"
alias liveX="bsub -q pcpgmwgs -R 'rusage[mem=16000]' -XF -n 1 -Is bash"
alias high="bsub -q pcpgmwgs -R 'rusage[mem=32000]' -n 1 -Is bash"
alias highX="bsub -q pcpgmwgs -R 'rusage[mem=32000]' -XF -n 1 -Is bash"
#alias alive="bsub -q pcpgmwgs -m pcpgmtest_hg -R 'rusage[mem=16000]' -n 1 -Is bash"
alias alive="bsub -q pcpgmwgs -R 'rusage[mem=16000]' -n 1 -Is bash"
alias aliveX="bsub -q pcpgmwgs -m pcpgmtest_hg -R 'rusage[mem=16000]' -XF -n 1 -Is bash"
alias olive="bsub -q pcpgmtest -m pcpgmwgs_hg -R 'rusage[mem=16000]' -n 1 -Is bash"
alias oliveX="bsub -q pcpgmtest -m pcpgmwgs_hg -R 'rusage[mem=16000]' -XF -n 1 -Is bash"

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
alias share='cd $SHR'

#people
alias bpt=become_pipeline_test
alias bpp=become_pipeline_prod

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
alias ls=ls

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



#viscap data dirs
export VISDATA=/scratch/pcpgm/jje16/projects/viscap/data
export SUCCESS=$VISDATA/success
export UNSUCCESS=$VISDATA/unsuccess

#call viscap
alias success=/scratch/pcpgm/jje16/projects/viscap/bin/call_success.sh
alias unsuccess=/scratch/pcpgm/jje16/projects/viscap/bin/call_unsuccess.sh
