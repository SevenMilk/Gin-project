#!/bin/bash

diff=1
d=`date +%Y/%m/%d -d "$1 - ${diff} day"`
dd=`date +%Y%m%d -d "$1 - ${diff} day"`
ddd=`date +%Y-%m-%d -d "$1"`
echo $d

python3 python/job.py