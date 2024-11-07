#!/bin/bash

echo "pegasus-aws-batch-delete.sh: "$@

# Args:
# $1 - workingdir
# $2 - prefix

# Note: job definitions can be deregistered but not deleted.
# Deregistered job definitions are deleted after 180 days, see https://docs.aws.amazon.com/batch/latest/APIReference/API_DeregisterJobDefinition.html.
pegasus-aws-batch \
    --conf ${1}/pegasusrc \
    --prefix ${2} \
    --delete \
    -q ${2}-job-queue \
    -j ${2}-job-definition:1 \
    --ce ${2}-compute-env
