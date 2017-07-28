#!/usr/bin/env sh
set -e

#optional password for svn as arg
PASS=$1

SVN=http://svn.dipr.partners.org/ngs
BLD=trunk


declare -A repos
repos=(
    ['file-mover']='file-mover' 
    ['asap']='asap' 
    ['NGS-DataMonitor']='data-monitor' 
    ['NGS-GigpadMonitor']='gigpad-monitor' 
    ['NGS-Deployer']='NGS-Deployer' 
    ['variant-reporting-annotation']='variant-reporting/annotation' 
    ['variant-reporting-detection']='variant-reporting/detection' 
    ['cnv']='cnv' 
    ['summary-sheet-generation']='summary-sheet-generation'  
    ['filter-illumina-reads']='filter-illumina-reads')




date
pwd

if [ -n "${PASS}" ]; then
	ARG='--password ${PASS}'
fi

SVN="svn co ${ARG} http://svn.dipr.partners.org/ngs"

for i in "${!repos[@]}"; do

	CMD="${SVN}/${repos[$i]}/trunk $i"

echo $CMD
	eval $CMD

	unset CMD
done

echo '--code base done.'

exit

