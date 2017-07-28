#!/usr/bin/env sh
set -e


#args
if [ -z $2 ]; then
        echo 'usage: asap.deploy.cluster.sh remote_deployment_dir svn_password'
	exit
fi

DIR=$1
PASS=$2


echo '::BEGIN DEPLOYMENT.'
date
pwd



#subversion
echo ''
echo '--pulling from subversion.'
svn co --password $PASS http://svn.dipr.partners.org/ngs/file-mover/trunk file-mover > /dev/null
svn co --password $PASS http://svn.dipr.partners.org/ngs/asap/trunk asap > /dev/null
svn co --password $PASS http://svn.dipr.partners.org/ngs/data-monitor/trunk NGS-DataMonitor > /dev/null
svn co --password $PASS http://svn.dipr.partners.org/ngs/gigpad-monitor/trunk NGS-GigpadMonitor > /dev/null
svn co --password $PASS http://svn.dipr.partners.org/ngs/NGS-Deployer/trunk NGS-Deployer > /dev/null
svn co --password $PASS http://svn.dipr.partners.org/ngs/variant-reporting/annotation/trunk variant-reporting-annotation > /dev/null
svn co --password $PASS http://svn.dipr.partners.org/ngs/variant-reporting/detection/trunk variant-reporting-detection > /dev/null
svn co --password $PASS http://svn.dipr.partners.org/ngs/summary-sheet-generation/trunk summary-sheet-generation > /dev/null
svn co --password $PASS http://svn.dipr.partners.org/ngs/filter-illumina-reads/trunk filter-illumina-reads > /dev/null
echo '--code base done.'

exit;
#fix configs
echo '!!please fix asap deployment config'
vi asap/config/ngs-dev.properties

echo '!!please fix file-mover config'
vi file-mover/FileMoverNGS-test.ini

echo '--proceeding.'

#java
echo ''
echo '--building java.'
cd NGS-DataMonitor
ant

cd ../NGS-GigpadMonitor
ant

cd ../asap
ant
echo '--java build done.'


echo ''
echo '--deploying to cluster.'
cd ../NGS-Deployer
sh ./deployClusterCode.sh pipeline_test@erisone.partners.org $DIR test
echo '--deployment script complete.'

echo ''
echo '::DEPLOYMENT SUCCESSFUL.'

exit

