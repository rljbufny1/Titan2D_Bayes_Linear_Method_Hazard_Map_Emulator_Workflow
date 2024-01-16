#!/bin/bash

# Create roles logged in as user with administrative access.

# Args:
# $1 - workingdir
# $2 - prefix

echo "pegasus-aws-batch.sh workingdir: "${1}" prefix: "${2}
echo "PWD: "${PWD}

# Need AWS BATCH Service Role named AWSBatchServiceRole.
# See https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html
# Need Amazon ECS Instance Role name ecsInstanceRole.
# See https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html
# Need IAM Role named batchJobRole.
# See https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/
# Also see https://docs.aws.amazon.com/batch/latest/userguide/compute_environment_parameters.html

cp -f ${1}/pegasusrc_template ${1}/pegasusrc

perl -i -pe"s~AMAZON_AWS_BATCH_PREFIX~${2}~g" ${1}/pegasusrc

pegasus-aws-batch \
    --conf ${1}/pegasusrc \
    --prefix ${2} \
    --create \
    --compute-environment ${1}/conf/compute-env.json \
    --job-definition ${1}/conf/job-definition.json \
    --job-queue ${1}/conf/job-queue.json
