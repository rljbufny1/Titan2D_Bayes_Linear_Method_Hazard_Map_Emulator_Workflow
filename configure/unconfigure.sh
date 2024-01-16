#!/bin/bash

cp -f -v ./aws_config_template ../submithost/.aws/config
cp -f -v ./aws_credentials_template ../submithost/.aws/credentials
cp -f -v ./pegasus_credentials_conf_template ../submithost/.pegasus/credentials.conf
cp -f -v ./pegasusrc_template ../submithost/emulator/pegasusrc_template
cp -f -v ./conf_job_definition_json_template ../submithost/emulator/conf/job-definition.json

cp -f -v ./build-and-push-docker-image-to-ECR_sh_template ../remotehost/build-and-push-docker-image-to-ECR.sh

