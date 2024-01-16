#!/bin/bash

# Executable launch script for the Pegasus workflow.
# Called with argument: "$@"
echo "$@"

tar -xzvf grassdata.tar.gz
/opt/titan_wsp/titan2d_bld/iccoptompmpi/bin/titan "$@" 2>&1
# rm -r grassdata

exitStatus=$?
exit ${exitStatus}
