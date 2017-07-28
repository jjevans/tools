# jje, 09182012
#echo ""
#echo jje, 09182012
#echo jje, 10012013
echo jje, 04252014

# Source global definitions
#if [ -f /etc/bashrc ]; then
#	. /etc/bashrc
#fi

####
##variables

##projects
#nva
export ALAMUTVM=alamut-ht1.dipr.partners.org
export NVA=/Users/jje16/Work/Tools/SVN/ngs/NVA/trunk
export NVACONF=$NVA/nva_conf.yml
export NVATEST=$NVA/support_script/test_run
alias nvarun="$NVA/va_exec.py"

##sys
export EDITOR=vi
export PS1="[\h:\W \!]: "
export DISPLAY=:0.0

##places
#work
export DATA=~/Work/Data
export PROJ=~/Work/Projects
export TOOL=~/Work/Tools
export MY=$TOOL/mybin
export SMB=~/Work/SMB

#svn
export SVN=~/Work/Tools/SVN
export NGS=$SVN/ngs
export SVNGROUP=$NGS/bioinfo
export SVNPEOPLE=$SVNGROUP/People
export ME=$SVNPEOPLE/Jason
export SVNPROJECT=$SVNGROUP/Projects

#external resources
export NCBIFTP='ftp.ncbi.nlm.nih.gov'

##tools
#apache
export APACHE=/etc/apache2
export APACHECONF=$APACHE/httpd.conf

#local gatk
export GATK_DIR=~/Work/Tools/GATK
export GATK=$GATK_DIR/gatk
export Q=$GATK_DIR/queue

#local galaxy instance
#export DRMAA_LIBRARY_PATH=/Library/Python/2.7/site-packages/
export GAL=~/Work/Tools/Galaxy/galaxy-dist
export GALAXY_DATA_INDEX_DIR=$GAL/tool-data
export JAVA_JAR_PATH=$GALAXY_DATA_INDEX_DIR/shared/jars/picard

##paths
export PATH=$ME/bin:$NVA:$NVA/support_script:~/Work/Tools/mybin:~/Work/Tools/MetaMap/public_mm/bin:~/Work/Tools/Jython:~/Work/Tools/scala-2.9.2/bin:/usr/local/mysql-5.5.28-osx10.6-x86_64/bin:/opt/local/bin:/opt/local/sbin:~/Work/Tools/MetaMap/public_mm/src/javaapi/dist:/Users/jje16/Work/Tools/vcftools-dist/vcftools_0.1.12a/bin:/Users/jje16/Work/Tools/vcftools-dist/vcftools_0.1.12a/perl:/Users/jje16/Work/Tools/FastQC/FastQC.app/Contents/Resources/Java:/Users/jje16/Work/Tools/bedtools:/Users/nva_user/Tools/bin:/usr/local/oracle/instantclient_11_2:/Users/jje16/Work/Tools/bin:/usr/local/pgsql/bin:/Library/Frameworks/R.framework/Resources/bin:$PATH

#programming language
export CLASSPATH=.:/Users/jje16/Work/Tools/javabin:/Users/jje16/Work/Tools/MetaMap/utsapi2_0:/Users/jje16/Work/Tools/MetaMap/public_mm/src/javaapi/build/classes:/Users/jje16/Work/Tools/MetaMap/public_mm/src/javaapi/dist:/Users/jje16/Work/Tools/Jython:~/Work/Tools/Tomcat/apache-tomcat-7.0.35-src/java:~/Work/Tools/JDBC:$CLASSPATH
export PERL5LIB=/Users/jje16/Work/Tools/SVN/ngs/bioinfo/People/Jason/lib:/Users/jje16/Work/Tools/mybin:/Users/jje16/Work/Tools/Galaxy/galaxy-dist/tools/partners:/Users/jje16/Work/Projects/SVN/Homopolymer/trunk:/Users/jje16/Work/Tools/vcftools/vcftools_0.1.10/perl:/Users/jje16/Work/Tools/BioPerl-1.6.1:$PERL5LIB
export PYTHONPATH=/Users/jje16/Work/Tools/SVN/ngs/NVA/trunk/modules:/Users/jje16/Work/Tools/SVN/ngs/bioinfo/People/Jason/lib:/Users/jje16/Work/Tools/mybin:$PYTHONPATH
export JAVA_HOME=`/usr/libexec/java_home`

##db
#oracle
export ORACLE_HOME=/usr/local/oracle/instantclient_11_2
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
export DYLD_LIBRARY_PATH=$ORACLE_HOME
#export LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH
export TNS_ADMIN=$ORACLE_HOME

####
##aliases

##apps
alias safari=/Applications/Safari.app/Contents/MacOS/Safari
alias firefox=/Applications/Firefox.app/Contents/MacOS/firefox

##places
#internal
alias eris='ssh jje16@erisone.partners.org'
alias erisX='ssh -YC jje16@erisone.partners.org'
alias erisftp='sftp jje16@erisone.partners.org'

alias ppm='ssh ppm.dipr.partners.org'
alias ppmftp='sftp ppm.dipr.partners.org'

alias rgs='ssh rgs06.research.partners.org'
alias rgsX='ssh -YC rgs06.research.partners.org'
alias pcpgm='ssh pcpgm.dipr.partners.org'
alias pcpgmftp='sftp jje16@pcpgm.dipr.partners.org'

alias sangertest='ssh jje16@pcpgm-sanger-gp-test.dipr.partners.org'
alias testftp='sftp jje16@pcpgm-sanger-gp-test.dipr.partners.org'
alias sangerprod='ssh jje16@pcpgm-sanger-gp.dipr.partners.org'
alias sangerprodftp='sftp jje16@pcpgm-sanger-gp.dipr.partners.org'

#hive user jje16, St1ngers2, user genome, Mouse@Mendel
alias chive='ssh genome@hive49-206.dipr.partners.org'
alias hive='ssh jje16@hive49-206.dipr.partners.org'
alias m2='ssh genome@mendel-too.hpcgg.partners.org'
# user genome, pass b1uekar5

alias pdp='ssh jje16@primerapp-new.dipr.partners.org'
alias pdpftp='sftp jje16@primerapp-new.dipr.partners.org'
alias pdpdev='ssh pdp-dev.dipr.partners.org'

#external
alias ncbiftp='ftp anonymous@$NCBIFTP'

#mount/unmount /data/pcpgm, NVA directories
alias mntpcpgm='mount -t smbfs //jje16@Rc-ndc-exds1.partners.org/pcpgm ~/Work/SMB/pcpgm'
alias umntpcpgm='umount ~/Work/SMB/pcpgm'
alias mntnva='mount -t smbfs //jje16@Sfa92/lmm4$ ~/Work/SMB/lmm4'
alias umntnva='diskutil unmount ~/Work/SMB/lmm4'
alias mntkdb='mount -t smbfs //jje16@Sfa92/lmm4$/Knowledge_Database ~/Work/SMB/sfa92'
alias umntkdb='diskutil unmount ~/Work/SMB/sfa92'

##bioinfo
#phenodb, phenotips
alias phenodb='ssh jje16@phenodb.dipr.partners.org'

#nva project
alias alamutvm='ssh jje16@alamut-ht1.dipr.partners.org'
alias alamutvmftp='sftp jje16@alamut-ht1.dipr.partners.org'
alias nvauser='sudo su - nva_user'
alias novelvm='ssh jje16@novel-assess.dipr.partners.org'
alias novelvmftp='sftp jje16@novel-assess.dipr.partners.org'

#nlm metamap
alias skr='/Users/jje16/Work/Tools/MetaMap/public_mm/bin/skrmedpostctl start'
alias noskr='/Users/jje16/Work/Tools/MetaMap/public_mm/bin/skrmedpostctl stop'

##commands
#my info
alias rc='vi ~/.bash_profile'
alias src='source ~/.bash_profile'
alias myip="echo $(curl -s http://queryip.net/ip/)"

#ftp
#alias ftp='lftp'

#ls
alias lrt='ls -lrt'
alias lscolor='ls --color'
alias lsall='ls -a'
alias lshuman='ls -h'
alias lsrecur='ls -R'

#du
alias duh='du -h'
alias dual='du -a'
alias dudepth='du --max-depth=2'

#grep
alias g='grep'
alias gv='grep -v'
alias gn='grep -n'
alias gct='grep -c'

#apps
alias bun=bunzip2
alias bbe="which bbedit;which bbdiff;which bbfind"

#show hidden files in finder
alias showhidden="defaults write com.apple.finder AppleShowAllFiles TRUE"

