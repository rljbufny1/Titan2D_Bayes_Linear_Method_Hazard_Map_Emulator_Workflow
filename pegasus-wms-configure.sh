#!/bin/bash

# Configure Amazon AWS configuration settings and credentials.

# Inputs:
# ~/.aws/config
# ~/.aws/credentials

if ! [ -f ~/.aws/config ]; then
    echo "~./aws/config is required to run this script."; return 2
fi

if ! [ -f ~/.aws/credentials ]; then
    echo "~./aws/credentials is required to run this script."; return 2
fi

AMAZON_AWS_ACCOUNT_ID=$(awk -F ' = ' '{if (! ($0 ~ /^;/) && $0 ~ /account_id/) print $2}' ~/.aws/config)
echo 'AMAZON_AWS_ACCOUNT_ID: '${AMAZON_AWS_ACCOUNT_ID}

AMAZON_AWS_REGION=$(awk -F ' = ' '{if (! ($0 ~ /^;/) && $0 ~ /region/) print $2}' ~/.aws/config)
echo 'AMAZON_AWS_REGION: '${AMAZON_AWS_REGION}

AMAZON_AWS_ACCESS_KEY_ID=$(awk -F ' = ' '{if (! ($0 ~ /^;/) && $0 ~ /aws_access_key_id/) print $2}' ~/.aws/credentials)
echo 'AMAZON_AWS_ACCESS_KEY_ID: '${AMAZON_AWS_ACCESS_KEY_ID}

AMAZON_AWS_SECRET_ACCESS_KEY=$(awk -F ' = ' '{if (! ($0 ~ /^;/) && $0 ~ /aws_secret_access_key/) print $2}' ~/.aws/credentials)
echo 'AMAZON_AWS_SECRET_ACCESS_KEY: '${AMAZON_AWS_SECRET_ACCESS_KEY}

# Get to a known state
cp -f -v ./remotehost/push-remotehostimage-to-ECR_sh_template ./remotehost/push-remotehostimage-to-ECR.sh

cp -f -v ./submithost/emulator/pegasusrc_template ./submithost/emulator/pegasusrc

cp -f -v ./submithost/amazon-aws-credentials/.aws/aws_config_template ./submithost/amazon-aws-credentials/.aws/config
cp -f -v ./submithost/amazon-aws-credentials/.aws/aws_credentials_template ./submithost/amazon-aws-credentials/.aws/credentials
cp -f -v ./submithost/amazon-aws-credentials/.pegasus/pegasus_credentials_conf_template ./submithost/amazon-aws-credentials/.pegasus/credentials.conf
cp -f -v ./submithost/pegasus-wms-configuration-files/job_definition_json_template ./submithost/pegasus-wms-configuration-files/job-definition.json
cp -f -v ./submithost/pegasus-wms-configuration-files/compute_env_json_template ./submithost/pegasus-wms-configuration-files/compute-env.json

perl -i -pe"s~AMAZON_AWS_ACCOUNT_ID~${AMAZON_AWS_ACCOUNT_ID}~g" ./remotehost/push-remotehostimage-to-ECR.sh
perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ./remotehost/push-remotehostimage-to-ECR.sh

perl -i -pe"s~AMAZON_AWS_ACCOUNT_ID~${AMAZON_AWS_ACCOUNT_ID}~g" ./submithost/emulator/pegasusrc
perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ./submithost/emulator/pegasusrc

perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ./submithost/amazon-aws-credentials/.aws/config
perl -i -pe"s~AMAZON_AWS_ACCESS_KEY_ID~${AMAZON_AWS_ACCESS_KEY_ID}~g" ./submithost/amazon-aws-credentials/.aws/credentials
perl -i -pe"s~AMAZON_AWS_SECRET_ACCESS_KEY~${AMAZON_AWS_SECRET_ACCESS_KEY}~g" ./submithost/amazon-aws-credentials/.aws/credentials
perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ./submithost/amazon-aws-credentials/.pegasus/credentials.conf
perl -i -pe"s~AMAZON_AWS_ACCESS_KEY_ID~${AMAZON_AWS_ACCESS_KEY_ID}~g" ./submithost/amazon-aws-credentials/.pegasus/credentials.conf
perl -i -pe"s~AMAZON_AWS_SECRET_ACCESS_KEY~${AMAZON_AWS_SECRET_ACCESS_KEY}~g" ./submithost/amazon-aws-credentials/.pegasus/credentials.conf

perl -i -pe"s~AMAZON_AWS_ACCOUNT_ID~${AMAZON_AWS_ACCOUNT_ID}~g" ./submithost/pegasus-wms-configuration-files/job-definition.json
perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ./submithost/pegasus-wms-configuration-files/job-definition.json

:


