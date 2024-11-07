#!/bin/bash

rm -f ./remotehost/build.log

cp -f ./remotehost/push-remotehostimage-to-ECR_sh_template ./remotehost/push-remotehostimage-to-ECR.sh

rm -f ./submithost/build.log

cp -f ./submithost/emulator/pegasusrc_template ./submithost/emulator/pegasusrc

cp -f ./submithost/amazon-aws-credentials/.aws/aws_config_template ./submithost/amazon-aws-credentials/.aws/config
cp -f ./submithost/amazon-aws-credentials/.aws/aws_credentials_template ./submithost/amazon-aws-credentials/.aws/credentials
cp -f ./submithost/amazon-aws-credentials/.pegasus/pegasus_credentials_conf_template ./submithost/amazon-aws-credentials/.pegasus/credentials.conf
cp -f ./submithost/pegasus-wms-configuration-files/job_definition_json_template ./submithost/pegasus-wms-configuration-files/job-definition.json
cp -f ./submithost/pegasus-wms-configuration-files/compute_env_json_template ./submithost/pegasus-wms-configuration-files/compute-env.json

if [ "$( ls -A './submithost/emulator/LOCAL/shared-storage' )" ]; then
   rm -rf ./submithost/emulator/LOCAL/shared-storage/*
fi

:
