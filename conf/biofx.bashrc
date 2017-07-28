#biofx .bashrc
# personalized medicine bioinformatics
# group settings
#created 03122015
#updated 00000000


##appearance
export PS1='\[\e[0;34m\][\[\e[1;34m\]\D{%D}:\[\e[0;34m\]\h//\W \[\e[0;32m\]\!\[\e[0;34m\]]:\[\e[m\] '


##locations
#erisone
export DATA=/data/pcpgm
export SCRATCH=/scratch/pcpgm
export VALID=/data/pcpgm/validation
export SHARE=$SCRATCH/share

#data: lmm/trc 
#/solexa_runs and wgs_processing
export NGS=$DATA/solexa/solexa_runs
alias ngs='cd $NGS'

#wgs
export WGS=$DATA/wgs
export WGS_PROC=$WGS/wgs_processing
alias wgs='cd $WGS_PROC'

#data: references
export REF=$SHARE/reference
export HG19=$REF/hg19/Homo_sapiens_assembly19.fasta

#projects
export ASAP=$DATA/asap-prod


##utils
#set your local SVN repository here, and your name
export SVN=
export ME=$SVN/ngs/bioinfo/People/YOURNAME
export BFX=$SVN/ngs/bioinfo/Project


##paths
##symlink any software to dir /share/software/current/bin and it's in your path
export PATH=$PATH:$SHARE/software/current/bin
export PERL5LIB=$PERL5LIB:$SHARE/software/current/lib/perl5
export PYTHONPATH=$PYTHONPATH:$SHARE/software/current/lib/python2.7


##modules
if [ -n "$MODULESHOME" ]; then
	#group
	module use /apps/modulefiles/lab/ppm

	#langs and environ
	module load R/3.1.1-asap

	#tools
	module load bedtools/default
	module load vcftools/default

	#module load bwa/0.7.10
	#module load gatk/default
	#module load samtools/default
	#module load snpeff/default
	#module load tabix/default
fi


##dbs
#oracle, biofx shared client
#export ORACLE_HOME=$SHARE/software/oracle/11.2/client64
#export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH
#export TNS_ADMIN=$SHARE/db/ora


##libs
export DRMAA_LIBRARY_PATH=$SHARE/local/lib/libdrmaa.so


##aliases
#for .bashrc ease
alias rc='$EDITOR ~/.bashrc'
alias src='source ~/.bashrc'

#create a file in home dir with snippits of good commands
alias useful='cat >> ~/useful_cmds.txt'
alias cmds='cat ~/useful_cmds.txt'

#lsf: interactive
alias alive="bsub -q pcpgmwgs -R 'rusage[mem=16000]' -n 1 -Is bash"
alias aliveX="bsub -q pcpgmwgs -m pcpgmtest_hg -R 'rusage[mem=16000]' -XF -n 1 -Is bash"
alias olive="bsub -q pcpgmtest -m pcpgmwgs_hg -R 'rusage[mem=16000]' -n 1 -Is bash"
alias oliveX="bsub -q pcpgmtest -m pcpgmwgs_hg -R 'rusage[mem=16000]' -XF -n 1 -Is bash"

#lsf: bsub
alias bsubwgs='bsub -q pcpgmwgs -m pcpgmwgs_hg'
alias bsubtest='bsub -q pcpgmwgs -m pcpgmtest_hg'
alias build='bsub_builder.py -R 8000 -n 1'

#utils
alias h="history | tail -500"
alias deep='du --max-depth=2'

alias g='grep'
alias gn='grep -n'
alias gc='grep -c'

alias javaj='java -Xms4g -Xmx32g -jar'

