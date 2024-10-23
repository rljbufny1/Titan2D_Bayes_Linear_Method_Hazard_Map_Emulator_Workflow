#!/bin/bash

echo "pegasus-analyzer.sh: "$@

# Args:
# $1 - working directory
# $2 - submit directory

pegasus-analyzer ${2} > ${1}/pegasus-analysis.txt
