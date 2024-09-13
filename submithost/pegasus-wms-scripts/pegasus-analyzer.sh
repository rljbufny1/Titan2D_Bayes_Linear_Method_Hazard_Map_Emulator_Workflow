#!/bin/bash

# Args:
# $1 - working directory
# $2 - submit directory

echo "pegasus-analyzer.sh working directory: "${1}" submit directory: "${2}

pegasus-analyzer ${2} > ${1}/pegasus-analysis.txt
