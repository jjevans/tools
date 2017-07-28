#%Module1.0
#biofx .bashrc
# personalized medicine bioinformatics
# group settings
#created 03122015
#updated 00000000

module-trace on
module-whatis	"BioFx: Partners Personalized Medicine Bioinformatics"

set dir_data "/data/pcpgm"
set dir_scratch "/scratch/pcpgm"

set dir_share "$dir_scratch/share"
set dir_ref "$dir_share/reference"
set dir_tool "$dir_share/software"
set dir_current "$dir_tool/current"


##appearance
set ps1 os.getenv('PS1')
if([string length [$ps1]] == 0){
	setenv PS1 '\[\e[0;34m\][\[\e[1;34m\]\D{%D}:\[\e[0;34m\]\h//\W \[\e[0;32m\]\!\[\e[0;34m\]]:\[\e[m\] '
}


##locations
#erisone
setenv DATA "$dir_data"
setenv SCRATCH "$dir_scratch"
setenv VALID "$dir_data/validation"
setenv SHARE "$dir_share"

#data: lmm/trc 
#/solexa_runs and wgs_processing
set dir_ngs "$dir_data/solexa/solexa_runs"
setenv NGS "$dir_ngs"
set-alias ngs 'cd $dir_ngs'

#wgs
set dir_wgs "$dir_data/wgs/wgs_processing"
setenv WGS "$dir_wgs"
set-alias wgs 'cd $WGS_PROC'

#data: references
setenv REF "$dir_ref"
setenv HG19 "$dir_ref/hg19/Homo_sapiens_assembly19.fasta"

#projects
setenv ASAP "$dir_data/asap-prod"


##utils
#set your set SVN repository here, and your name
set dir_svn ''
setenv SVN "$dir_svn"
setenv ME "$dir_svn/ngs/bioinfo/People/YOURNAME"
setenv BFX "$dir_svn/ngs/bioinfo/Project"


##paths
##symlink any software to dir /share/software/current/bin and it's in your path
append-path PATH "$dir_current/bin"
append-path PERL5LIB "$dir_current/lib/perl5"
append-path PYTHONPATH "$dir_current/lib/python2.7"


##modules
#group
#module use /apps/modulefiles/lab/ppm

#langs and environ
load R/3.1.1-asap

#tools
load bedtools/default
load vcftools/default

#load bwa/0.7.10
#load gatk/default
#load samtools/default
#load snpeff/default
#load tabix/default


##dbs
#oracle, biofx shared client
set ora_home "$dir_tool/oracle/11.2/client64"
#setenv ORACLE_HOME "$ora_home"
#prepend-path LD_LIBRARY_PATH "$ora_home/lib"
#setenv TNS_ADMIN="$dir_share/db/ora"


##libs
setenv DRMAA_LIBRARY_PATH "$dir_share/set/lib/libdrmaa.so"


##set-aliases
#for .bashrc ease
set editor os.getenv("EDITOR")
if { [string compare $[editor]] == 0 } {
	set-alias rc 'os.getenv("EDITOR") ~/.bashrc'
else
	set-alias rc 'vi ~/.bashrc'
end

set-alias src 'source ~/.bashrc'

#create a file in home dir with snippits of good commands
set-alias useful 'cat >> ~/useful_cmds.txt'
set-alias cmds 'cat ~/useful_cmds.txt'

#lsf: interactive
set-alias alive "bsub -q pcpgmwgs -R 'rusage[mem=16000]' -n 1 -Is bash"
set-alias aliveX "bsub -q pcpgmwgs -m pcpgmtest_hg -R 'rusage[mem=16000]' -XF -n 1 -Is bash"
set-alias olive "bsub -q pcpgmtest -m pcpgmwgs_hg -R 'rusage[mem=16000]' -n 1 -Is bash"
set-alias oliveX "bsub -q pcpgmtest -m pcpgmwgs_hg -R 'rusage[mem=16000]' -XF -n 1 -Is bash"

#lsf: bsub
set-alias bsubwgs 'bsub -q pcpgmwgs -m pcpgmwgs_hg'
set-alias bsubtest 'bsub -q pcpgmwgs -m pcpgmtest_hg'
set-alias build 'bsub_builder.py -R 8000 -n 1'

#utils
set-alias h "history | tail -500"
set-alias deep 'du --max-depth=2'

set-alias g 'grep'
set-alias gn 'grep -n'
set-alias gc 'grep -c'

set-alias javaj 'java -Xms4g -Xmx32g -jar'

