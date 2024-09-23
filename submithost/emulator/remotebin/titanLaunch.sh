#!/bin/bash

# Executable launch script for the Pegasus workflow.
# Called with arguments: "$@"
echo "titanLaunch.sh $@"

tar -xzvf grassdata.tar.gz
/opt/titan_wsp/titan2d_bld/iccoptompmpi/bin/titan "$@"
# rm -r grassdata

:
