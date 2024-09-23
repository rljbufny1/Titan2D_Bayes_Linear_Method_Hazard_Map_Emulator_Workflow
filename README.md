# Titan2D Hazard Map Emulator Workflow

This workflow tool produces [Titan2D](https://github.com/TITAN2D/titan2d) hazard maps that display the probability of a volcanic flow depth reaching a critical height following a premonitory event.

Titan2D is a computer model for simulating granular avalanches over digital elevation models (DEMs) of natural terrian. The Titan2D hazard maps are constructed by creating a statistical surrogate model of the Titan2D computer model, requiring numerous executions of the Titan2D computer model. The Pegasus Workflow Management System (WMS) provides the structured platform for automating and managing these numerous executions, including staging the jobs, distributing the work, submitting the jobs to run in parallel, as well as handling data flow dependencies and overcoming job failures.

This tool is designed to follow the Pegasus WMS Amazon Batch execution environment which in turn is based on the Amazon AWS Fetch & Run Procedure. See [Pegasus WMS Documentation](https://pegasus.isi.edu/documentation) for more information. 

This tool runs two Docker containers, a submit host Docker container and a remote host Docker container. 

The submit host Docker container's image contains software required to implement the Titan2D Hazard Map Emulator workflow including HTCondor and the Pegasus WMS.

The remote host Docker container's image contains software to run Titan2D and includes the bash fetch-and-run script and the fetch-and-run script ENTRYPOINT for pegasus-aws-batch.

## Requirements:

See [Pegasus WMS Deployment Scenarios](https://pegasus.isi.edu/documentation/user-guide/deployment-scenarios.html), Amazon AWS Batch, for more information on the one time setup required for Pegasus AWS Batch.

### Pegasus WMS requires Amazon AWS configuration and credential files for Pegasus AWS Batch:

~/.aws/conf<br />
~/.aws/credentials

### Pegasus WMS requires three credential files for Pegasus AWS Batch:

.aws/conf:<br/>
[default]<br/>
region = us-east-2

.aws/credentials:<br/>
[default]<br/>
aws_access_key_id = *<br/>
aws_secret_access_key = *

.pegasus/credentials.conf:<br/>
[amazon]<br/>
endpoint = https://s3.amazonaws.com<br/>
#Max object size in MB<br/>
max_object_size = 1024<br/>
multipart_uploads = True<br/>
ranged_downloads = True<br/>
[user@amazon]<br/>
access_key = *<br/>
secret_key = *

where * is replaced with your Amazon AWS credentials information.

### emulator.ipynb:

This Jupyter notebook provides the interface for running the Titan2D Hazard Map Emulator Workflow.

### pegasus-wms-configuration-scripts directory
 
- **Note: source configure.sh must be completed before building the submit host and the remote host Docker images.**

- Update creditionals template files in the remotehost and rsubmithost directories.

	cd ./pegasus-wms-configuration_scripts<br>
	source configure.sh<br>

### remotehost directory

- Create an Amazon AWS Elastic Container repository for the remote host Docker image.
- Build the remote host Docker image.
- Upload the remote host Docker image to the created repository.

	cd ./remotehost<br>
	docker image build -t remotehostimage . 2>&1 | tee build.log<br>
	source ./push-docker-image-to-ECR.sh<br>

### submithost directory

- Build the submit host Docker image.
- Run the submit host Docker Image.
- Open the submit host Docker image's Jupyter notebook emulator.ipynb.

	cd ./submithost<br>
	docker image build -t submithostimage . 2>&1 | tee build.log<br>
	docker run --privileged --rm -v $PWD/emulator/LOCAL/shared-storage:/home/submithost/emulator/LOCAL/shared-storage -p 9999:8888 submithostimage

When the Sending DC_SET_READY message appears, open a web browser and enter the url localhost:9999/apps/emulator.ipynb and enter the password emulator. This opens the emulator.ipynb Jupyter notebook in [Appmode](https://github.com/oschuett/appmode#). Results for running a workflow are written to the mounted ./submithost/emulator/LOCAL/shared-storage directory.