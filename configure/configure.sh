#!/bin/bash

# Configure Amazon AWS configuration settings and credentials.

# Inputs:
# ~/.aws/config
# ~/.aws/credentials

AMAZON_AWS_ACCOUNT_ID=$(awk -F ' = ' '{if (! ($0 ~ /^;/) && $0 ~ /account_id/) print $2}' ~/.aws/config)
echo 'AMAZON_AWS_ACCOUNT_ID: '${AMAZON_AWS_ACCOUNT_ID}

AMAZON_AWS_REGION=$(awk -F ' = ' '{if (! ($0 ~ /^;/) && $0 ~ /region/) print $2}' ~/.aws/config)
echo 'AMAZON_AWS_REGION: '${AMAZON_AWS_REGION}

AMAZON_AWS_ACCESS_KEY_ID=$(awk -F ' = ' '{if (! ($0 ~ /^;/) && $0 ~ /aws_access_key_id/) print $2}' ~/.aws/credentials)
echo 'AMAZON_AWS_ACCESS_KEY_ID: '${AMAZON_AWS_ACCESS_KEY_ID}

AMAZON_AWS_SECRET_ACCESS_KEY=$(awk -F ' = ' '{if (! ($0 ~ /^;/) && $0 ~ /aws_secret_access_key/) print $2}' ~/.aws/credentials)
echo 'AMAZON_AWS_SECRET_ACCESS_KEY: '${AMAZON_AWS_SECRET_ACCESS_KEY}

perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ../submithost/.aws/config
perl -i -pe"s~AMAZON_AWS_ACCESS_KEY_ID~${AMAZON_AWS_ACCESS_KEY_ID}~g" ../submithost/.aws/credentials
perl -i -pe"s~AMAZON_AWS_SECRET_ACCESS_KEY~${AMAZON_AWS_SECRET_ACCESS_KEY}~g" ../submithost/.aws/credentials
perl -i -pe"s~AMAZON_AWS_ACCESS_KEY_ID~${AMAZON_AWS_ACCESS_KEY_ID}~g" ../submithost/.pegasus/credentials.conf
perl -i -pe"s~AMAZON_AWS_SECRET_ACCESS_KEY~${AMAZON_AWS_SECRET_ACCESS_KEY}~g" ../submithost/.pegasus/credentials.conf
perl -i -pe"s~AMAZON_AWS_ACCOUNT_ID~${AMAZON_AWS_ACCOUNT_ID}~g" ../submithost/emulator/pegasusrc_template
perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ../submithost/emulator/pegasusrc_template
perl -i -pe"s~AMAZON_AWS_ACCOUNT_ID~${AMAZON_AWS_ACCOUNT_ID}~g" ../submithost/emulator/conf/job-definition.json
perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ../submithost/emulator/conf/job-definition.json

perl -i -pe"s~AMAZON_AWS_ACCOUNT_ID~${AMAZON_AWS_ACCOUNT_ID}~g" ../remotehost/build-and-push-docker-image-to-ECR.sh
perl -i -pe"s~AMAZON_AWS_REGION~${AMAZON_AWS_REGION}~g" ../remotehost/build-and-push-docker-image-to-ECR.sh
