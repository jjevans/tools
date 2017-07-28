#!/usr/bin/env sh
set -e

#call deployClusterCode with args provided already
#args
if [ -z $1 ]; then
        echo 'usage: asap.ppm.cluster.sh remote_deployment_dir'
	exit
fi

DIR=$1

echo ''
echo '--deploying to cluster.'
cd ../NGS-Deployer
#sh ./deployClusterCode.sh pipeline_test@erisone.partners.org $DIR test
sh ./deployClusterCode.sh pipeline_test@erisone.partners.org $DIR dev
echo '--deployment script complete.'

echo ''
echo '::DEPLOYMENT SUCCESSFUL.'

exit

