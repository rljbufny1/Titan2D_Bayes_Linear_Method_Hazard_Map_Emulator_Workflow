#!/bin/bash

cp -f -v ./remotehost/push-remotehostimage-to-ECR_sh_template ./remotehost/push-remotehostimage-to-ECR.sh

cp -f -v ./submithost/emulator/pegasusrc_template ./submithost/emulator/pegasusrc

cp -f -v ./submithost/amazon-aws-credentials/.aws/aws_config_template ./submithost/amazon-aws-credentials/.aws/config
cp -f -v ./submithost/amazon-aws-credentials/.aws/aws_credentials_template ./submithost/amazon-aws-credentials/.aws/credentials
cp -f -v ./submithost/amazon-aws-credentials/.pegasus/pegasus_credentials_conf_template ./submithost/amazon-aws-credentials/.pegasus/credentials.conf
cp -f -v ./submithost/pegasus-wms-configuration-files/job_definition_json_template ./submithost/pegasus-wms-configuration-files/job-definition.json
cp -f -v ./submithost/pegasus-wms-configuration-files/compute_env_json_template ./submithost/pegasus-wms-configuration-files/compute-env.json

rm -rf ./submithost/emulator/LOCAL/shared-storage/*

:
