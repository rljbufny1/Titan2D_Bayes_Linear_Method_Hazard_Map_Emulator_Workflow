#!/bin/bash

echo "pegasus-statistics.sh: "$@

# Args:
# $1 - working directory
# $2 - submit directory

pegasus-statistics ${2} > ${1}/pegasus-statistics.txt
