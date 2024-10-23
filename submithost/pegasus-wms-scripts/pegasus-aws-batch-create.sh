#!/bin/bash

echo "pegasus-aws-batch-create.sh: "$@

# Args:
# $1 - workingdir
# $2 - prefix

# Need AWS BATCH Service Role named AWSBatchServiceRole.
# See https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html
# Need Amazon ECS Instance Role named ecsInstanceRole.
# See https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html
# Need IAM Role named batchJobRole.
# See https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/
# Also see https://docs.aws.amazon.com/batch/latest/userguide/compute_environment_parameters.html

# Roles are created logged in as an IAM user with administrative access.

cp -f ${1}/pegasusrc_template ${1}/pegasusrc

perl -i -pe"s~AMAZON_AWS_BATCH_PREFIX~${2}~g" ${1}/pegasusrc

pegasus-aws-batch \
    --conf ${1}/pegasusrc \
    --prefix ${2} \
    --create \
    --ce ${1}/conf/compute-env.json \
    -j ${1}/conf/job-definition.json \
    -q ${1}/conf/job-queue.json

:
