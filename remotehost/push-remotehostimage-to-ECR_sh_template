#!/bin/bash

# Before running this script:

# Need to create the Elastic Container Registry repository for the remotehostimage Docker image using the Amazon AWS console if it does not exist. Name the repository: remotehostimage.

# The following requires proper credentials are stored in ~/.aws/conf and ~/.aws/credentials.

# Upload the remotehostimage Docker image to the Elastic Container Registry remotehostimage repository:

aws ecr get-login-password --region AMAZON_AWS_REGION | docker login --username AWS --password-stdin AMAZON_AWS_ACCOUNT_ID.dkr.ecr.AMAZON_AWS_REGION.amazonaws.com

# Also see ../submithost/pegasus-wms-configuration-files/job-definition.json
docker tag remotehostimage:latest AMAZON_AWS_ACCOUNT_ID.dkr.ecr.AMAZON_AWS_REGION.amazonaws.com/remotehostimage:latest

docker push AMAZON_AWS_ACCOUNT_ID.dkr.ecr.AMAZON_AWS_REGION.amazonaws.com/remotehostimage:latest
