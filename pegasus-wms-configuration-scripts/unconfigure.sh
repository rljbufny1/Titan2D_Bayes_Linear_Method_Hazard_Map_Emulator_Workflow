#!/bin/bash

cp -f -v ./build-and-push-docker-image-to-ECR_sh_template ../remotehost/build-and-push-docker-image-to-ECR.sh

cp -f -v ./aws_config_template ../submithost/amazon-aws-credentials/.aws/config
cp -f -v ./aws_credentials_template ../submithost/amazon-aws-credentials/.aws/credentials
cp -f -v ./pegasus_credentials_conf_template ../submithost/amazon-aws-credentials/.pegasus/credentials.conf
cp -f -v ./conf_job_definition_json_template ../submithost/pegasus-wms-configuration-files/job-definition.json
cp -f -v ./pegasusrc_template ../submithost/pegasus-wms-configuration-files/pegasusrc_template
