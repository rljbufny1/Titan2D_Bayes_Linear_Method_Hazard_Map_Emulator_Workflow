#!/bin/bash

# Need to create the Elastic Container Registry repository for the image first using the Amazon AWS console if it does not exist.

# The following requires proper credentials are stored in ~/.aws/conf and ~/.aws/credentials.

# When an image is created or updated using docker image build -t remotehostimage .,
# upload the image to the Elastic Container Registry repository:

aws ecr get-login-password --region AMAZON_AWS_REGION | docker login --username AWS --password-stdin AMAZON_AWS_ACCOUNT_ID.dkr.ecr.AMAZON_AWS_REGION.amazonaws.com

docker tag remotehostimage:latest AMAZON_AWS_ACCOUNT_ID.dkr.ecr.AMAZON_AWS_REGION.amazonaws.com/remotehostimage:latest

docker push AMAZON_AWS_ACCOUNT_ID.dkr.ecr.AMAZON_AWS_REGION.amazonaws.com/remotehostimage:latest

# When an image is created,
# modify ../submithost/emulator/conf/job-definition.json and set the image name for the image.
