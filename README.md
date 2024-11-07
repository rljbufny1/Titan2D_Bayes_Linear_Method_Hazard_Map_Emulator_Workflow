# Titan2D Hazard Map Emulator Workflow

This workflow tool produces [Titan2D](https://github.com/TITAN2D/titan2d) hazard maps that display the probability of a volcanic flow depth reaching a critical height following a premonitory volcanic eruption event.

Titan2D is a computer model for simulating granular avalanches over digital elevation models (DEMs) of natural terrain. The Titan2D hazard maps are constructed by creating a statistical surrogate model of the Titan2D computer model, requiring numerous executions of the Titan2D computer model and the emulator's uncertainty quantification (UQ) software. See [Workflows for Construction of Spatio-Temporal Probabilistic Maps for Volcanic Hazard Assessment](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.744655) for more information.

The [Pegasus Workflow Management System (WMS)](https://pegasus.isi.edu) provides the structured platform for automating and managing these numerous executions, including staging the jobs, distributing the work, submitting the jobs to run in parallel, as well as handling data flow dependencies and overcoming job failures. This tool is designed to follow the Pegasus WMS, Amazon AWS Batch deployment scenario, which, in turn, is based on the [Amazon AWS Fetch & Run Example](https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/). See the [Welcome to Pegasus WMS’s documentation! Deployment Scenarios](https://pegasus.isi.edu/documentation/user-guide/deployment-scenarios.html), Amazon AWS Batch section, for more information. 

This tool runs two Docker images, a remotehostimage Docker image and a submithostimage Docker image. The remotehostimage Docker image is the Fetch & Run Docker image and contains software to run Titan2D and the emulator's UQ software, and, also includes the Bash Fetch & Run script and ENTRYPOINT. The submithostimage Docker image contains the software required to implement the workflow, including a Jupyter Notebook as the interface for running the workflow, HTCondor, and the Pegasus WMS.

## One-Time Amazon AWS Batch Setup

This tool requires that you complete the following prerequisites for configuring Amazon AWS Batch.

- Create an IAM account and an IAM user with administrative access. See [Create IAM account and administrative user](https://docs.aws.amazon.com/batch/latest/userguide/create-an-iam-account.html) for information on how to do this. Create an access key pair for the IAM user. See [Manage access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for information on how to do this.

- Sign in as the IAM user and create the IAM roles required for Pegasus Amazon AWS Batch. These are an AWS Batch Service IAM Role named AWSBatchServiceRole, an Amazon Elastic Container Service (ECS) Instance Role named ecsInstanceRole, and an IAM Role named batchJobRole. See the Pegasus WMS 
[Deployment Scenarios](https://pegasus.isi.edu/documentation/user-guide/deployment-scenarios.html), Amazon AWS Batch section, for more information.

- Sign in as the IAM user and create a Virtual Private Cloud (VPC) and security group for your Amazon AWS Region. See [Create a VPC](https://docs.aws.amazon.com/batch/latest/userguide/create-a-vpc.html) and [Create a security group](https://docs.aws.amazon.com/batch/latest/userguide/create-a-base-security-group.html) for information on how to do this.

- Install the Amazon AWS CLI on your personal computer. See [Getting started with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) for more information on how to do this.

## Configure Pegasus Amazon AWS Batch

AWS Batch comprises four components for a workflow: a compute environment, a job definition, a job queue, and the jobs. Pegasus Amazon AWS Batch provides an interface for creating and managing these AWS Batch components. To do this, Pegasus requires an AWS credential file, an AWS S3 configuration file, and JSON-formatted information catalogs. These files contain fields that reference your AWS authorization credentials. See the Pegasus WMS [Deployment Scenarios](https://pegasus.isi.edu/documentation/user-guide/deployment-scenarios.html), Amazon AWS Batch section, for more information.

### Configuration Requirements

This tool requires two AWS authorization credentials files: ~/.aws/config and ~/.aws/credentials. 

- Required contents of the ~/.aws/config file:<br/>
[default]<br/>
account_id = *<br />
region = *

- Required contents of the ~/.aws/credentials file:<br/>
[default]<br/>
aws_access_key_id = *<br />
aws_secret_access_key = *

	Where * is replaced with your IAM account and IAM user authorization credentials.

### Configuration Command
	
This tool's ./remosthost and ./submithost directories contain templates for the files that Pegasus requires. The ./pegasus-wms-configure.sh Bash script configures these files with your AWS authorization credentials.

- **Note: source ./pegasus-wms-configure.sh must be executed before building the remotehostimage and submithostimage Docker images.**

## Build the Docker Images

### Build the remotehostimage Docker image and push the image to the Amazon Elastic Cloud Registry (ECR).

- Create an Amazon AWS Elastic Container Repository (ECR) for your Amazon AWS Region. See [Creating an Amazon ECR private repository to store images](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html) for information on how to do this. Name the repository: remotehostimage.
- source ./pegasus-wms-configure.sh
- cd ./remotehost<br>
- docker image build -t remotehostimage . 2>&1 | tee build.log<br>
- source ./push-remotehostimage-to-ECR.sh<br>

### Build and submithostimage Docker image

- source ./pegasus-wms-configure.sh<br>
- cd ./submithost<br>
- docker image build -t submithostimage . 2>&1 | tee build.log<br>

## Run the Workflow

### Run the submithostimage Docker image

 - docker run --privileged --rm -v $PWD/emulator/LOCAL/shared-storage:/home/submithost/emulator/LOCAL/shared-storage -p 9999:8888 submithostimage

### Open the emulator.ipynb Jupyter Notebook and Run the Workflow

- The emulator.ipynb Jupyter Notebook provides the interface for running the workflow.

- When the docker run Sending DC_SET_READY message appears, open a web browser and enter the URL localhost:9999/apps/emulator.ipynb and enter the password emulator. This opens the emulator.ipynb Jupyter notebook in [Appmode](https://github.com/oschuett/appmode#). To open the emulator.ipynb Jupyter notebook in Edit Mode, enter the URL localhost:9999/notebooks/emulator.ipynb, enter the password emulator, and select Kernel / Restart & Run All.
 
-  Follow the processing steps in emulator.ipynb to set up and run the workflow. Setup includes selecting a volcano, setting the material model and pile parameters for the selected volcano's eruption, setting parameters for the emulator's UQ software, selecting a VPC subnet and security group, as well as running a script that further configures the JSON-formatted information catalogs that Pegasus requires with your defined parameters.

### Stop the submithostimage Docker container

- Log out of the emulator.ipynb Jupyter Notebook and enter Ctrl+C to stop the running Docker container.

## Workflow Results

- Results and interim files generated for running a workflow are stored in the mounted ./submithost/emulator/LOCAL/shared-storage directory.

- Results include the Hazard_Report.pdf file, which contains information on the probability of a volcanic flow depth reaching a critical height at specific locations. 

