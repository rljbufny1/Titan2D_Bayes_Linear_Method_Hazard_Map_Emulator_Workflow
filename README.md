# Titan2D Hazard Map Emulator Workflow

This workflow tool produces Titan2D hazard maps that display the probability of a volcanic flow depth reaching a critical height following a premonitory event.

Titan2D is a computer model for simulating granular avalanches over digital elevation models (DEMs) of natural terrian. The Titan2D hazard maps are constructed by creating a statistical surrogate model of the Titan2D computer model, requiring numerous executions of the Titan2D computer model. The Pegasus Workflow Management System (WMS) provides the structured platform for automating and managing these numerous executions, including staging the jobs, distributing the work, submitting the jobs to run in parallel, as well as handling data flow dependencies and overcoming job failures.

This tool is designed to follow the Pegasus WMS Amazon Batch execution environment which in turn is based on the Amazon AWS Fetch & Run Procedure. See [Pegasus WMS Documentaiton](https://pegasus.isi.edu/documentation) for more information.

This tool runs two Docker containers, a submit host Docker container and a remote host Docker container. 

The submit host Docker container's image contains software required to implement the Titan2D Hazard Map Emulator workflow including HTCondor and the Pegasus WMS.

The remote host Docker container's image includes the bash fetch-and-run script and the fetch-and-run script ENTRYPOINT for pegasus-aws-batch.

## Requirements:

### Amazon AWS Configuration and Credential Files:

~/.aws/conf<br />
~/.aws/credentials

See [Amazon AWS Configuration and Credential File Setting](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for more information.

Example conf and credential file formats:

conf:

[default]<br />
account_id = *<br />
region = * 

credentials:

[default]<br />
aws_access_key_id = *<br>
aws_secret_access_key = *

Where * is replaced with your Amazon AWS configuration and credential information.

Note: see ./submithost/emulator/pegasusrc for a note on region usage for Pegasus WMS. 

### configure directory
 
**Note: source configure.sh must be completed before building the submit host an remote host Docker images.**

- Update template files in the submithost and remotehost directories.

	cd ./configure<br>
	source configure.sh<br>

### remotehost directory

- Create an Amazon AWS Elastic Container repository for the remote host Docker image.
- Build the remote host Docker image.
- Upload the remote host Docker image to the created repository.

	cd ./remotehost<br>
	docker image build -t remotehostimage . 2>&1 | tee build.log<br>
	source ./build-and-push-docker-image-to-ECR.sh<br>

### submithost directory

- Build the submit host Docker image.
- Run the submit host Docker Image.
- Open the submit host Docker image's Jupyter notebook emulator.ipynb.

	cd ./submithost<br>
	docker image build -t submithostimage . 2>&1 | tee build.log<br>
	docker run --privileged --rm -p 9999:8888 submithostimage

When the Sending DC_SET_READY message appears, open a web browser and enter the url localhost:9999, enter the password emulator and open emulator.ipynb.

### emulator.ipynb:

This Jupyter notebook provides the interface for running the Titan2D Hazard Map Emulator Workflow.
