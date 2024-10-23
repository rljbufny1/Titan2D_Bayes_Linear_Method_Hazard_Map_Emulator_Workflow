#!/bin/bash

# rlj - bash script to update pegasus aws batch configuration files based on user selected parameters.

echo "aws-batch-configure.sh: $@"

# Args:
AMAZON_AWS_JOB_DEFINITION_MEMORY=${1}
AMAZON_AWS_COMPUTE_ENV_SUBNET=${2}
AMAZON_AWS_COMPUTE_ENV_SECURITY_GROUP=${3}

# Get to a known state
cp -f -v ./conf/job_definition_json_template ./conf/job-definition.json
cp -f -v ./conf/compute_env_json_template ./conf/compute-env.json

perl -i -pe"s~AMAZON_AWS_JOB_DEFINITION_MEMORY~${AMAZON_AWS_JOB_DEFINITION_MEMORY}~g" ./conf/job-definition.json

perl -i -pe"s~AMAZON_AWS_COMPUTE_ENV_SUBNET~${AMAZON_AWS_COMPUTE_ENV_SUBNET}~g" ./conf/compute-env.json
perl -i -pe"s~AMAZON_AWS_COMPUTE_ENV_SECURITY_GROUP~${AMAZON_AWS_COMPUTE_ENV_SECURITY_GROUP}~g" ./conf/compute-env.json
