#!/usr/bin/env sh
set -e


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

exit

