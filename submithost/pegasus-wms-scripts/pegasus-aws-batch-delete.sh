#!/bin/bash

# Delete roles logged in as user with administrative access.

# Args:
# $1 - workingdir
# $2 - prefix

echo "pegasus-aws-batch-delete.sh workingdir: "${1}" prefix: "${2}
echo "PWD: "${PWD}

pegasus-aws-batch \
    --conf ${1}/pegasusrc \
    --prefix ${2} \
    --delete \
    --job-queue ${2}-job-queue \
    --job-definition ${2}-job-definition \
    --compute-environment ${2}-compute-env
 

