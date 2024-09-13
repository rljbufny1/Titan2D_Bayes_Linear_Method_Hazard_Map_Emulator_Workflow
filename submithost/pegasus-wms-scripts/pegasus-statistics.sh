#!/bin/bash

# Args:
# $1 - working directory
# $2 - submit directory

echo "pegasus-statistics.sh working directory: "${1}" submit directory: "${2}

pegasus-statistics ${2} > ${1}/pegasus-statistics.txt
