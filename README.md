# Titan2D Hazard Map Emulator Workflow

This workflow tool produces [Titan2D](https://github.com/TITAN2D/titan2d) hazard maps that display the probability of a volcanic flow depth reaching a critical height following a premonitory volcanic eruption event.

Titan2D is a computer model for simulating granular avalanches over digital elevation models (DEMs) of natural terrain. The Titan2D hazard maps are constructed by creating a statistical surrogate model of the Titan2D computer model, requiring numerous executions of the Titan2D computer model and the emulator's uncertainty quantification (UQ) software. See [Workflows for Construction of Spatio-Temporal Probabilistic Maps for Volcanic Hazard Assessment](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.744655) for more information.

The [Pegasus Workflow Management System (WMS)](https://pegasus.isi.edu) provides the structured platform for automating and managing these numerous executions, including staging the jobs, distributing the work, submitting the jobs to run in parallel, as well as handling data flow dependencies and overcoming job failures. This tool is designed to follow the Pegasus WMS, Amazon AWS Batch Deployment Scenario, which, in turn, is based on the AWS Fetch & Run Procedure. See [Welcome to Pegasus WMS’s documentation!](https://pegasus.isi.edu/documentation) and [Creating a Simple "Fetch & Run" AWS Batch Job](https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/) for more information. 

This tool runs two Docker containers, a remotehostimage Docker container and a submithostimage Docker container. The Fetch & Run Docker image, remotehostimage, contains software to run Titan2D and the emulator's UQ software, and, also includes the Bash Fetch & Run script and ENTRYPOINT. The submithostimage Docker image contains the software required to implement the workflow, including a Jupyter Notebook as the interface for running the workflow, HTCondor, and the Pegasus WMS.

## Configure the Tool

This tool requires that you complete the prerequisites for configuring AWS Batch, which include creating an IAM user account with administrative access, creating required IAM roles and key pairs, and creating a Virtual Private Cloud (VPC) and security group.  See [Complete the AWS Batch prerequisites](https://docs.aws.amazon.com/batch/latest/userguide/get-set-up-for-aws-batch.html) for information on how to do this.

Specific IAM roles required for the AWS Fetch & Run Procedure are an AWS BATCH Service Role named AWSBatchServiceRole, an Elastic Container Service (ECS) Instance Role named ecsInstanceRole, and an IAM Role named batchJobRole. See the Pegasus WMS 
[Deployment Scenarios](https://pegasus.isi.edu/documentation/user-guide/deployment-scenarios.html), AWS Batch documentation, for more information.

AWS Batch comprises four components for a workflow: a compute environment, a job definition, a job queue, and the jobs. The Pegasus WMS provides an interface for creating and managing these AWS Batch components. To do this, Pegasus requires an AWS credential file, an AWS S3 configuration file, and JSON-formatted information catalogs. These files contain fields that reference your defined AWS Batch configurations. See the Pegasus WMS [Deployment Scenarios](https://pegasus.isi.edu/documentation/user-guide/deployment-scenarios.html), AWS Batch documentation, for more information.

### Configuration Requirements

This tool requires that you have the Amazon AWS CLI installed on your personal computer. See [Getting started with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) for more information.

This tool also requires two AWS authorization credentials files: ~/.aws/config and ~/.aws/credentials. 

- Required contents of the ~/.aws/config file:<br/>
[default]<br/>
account_id = *<br />
region = *

- Required contents of the ~/.aws/credentials file:<br/>
[default]<br/>
aws_access_key_id = *<br />
aws_secret_access_key = *

	Where * is replaced with your AWS authorization credentials.

### Configuration Command
	
This tool's ./remosthost and ./submithost directories contain templates for the files that Pegasus requires. The ./pegasus-wms-configure.sh Bash script configures these files with your AWS authorization credentials.

**Note: source ./pegasus-wms-configure.sh must be executed before building the remotehostimage and submithostimage Docker images.**

- source ./pegasus-wms-configure.sh<br>

## Build the Docker Images

### Build the remotehostimage Docker image and push the image to the Amazon Elastic Cloud Registry (ECR).

- Create an Amazon AWS Elastic Container Repository (ECR) for your Amazon AWS Region. See [Creating an Amazon ECR private repository to store images](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html) for information on how to do this. Name the repository: remotehostimage.
- cd ./remotehost<br>
- docker image build -t remotehostimage . 2>&1 | tee build.log<br>
- source ./push-remotehostimage-to-ECR.sh<br>

### Build and run the submithostimage Docker image


- cd ./submithost<br>
- docker image build -t submithostimage . 2>&1 | tee build.log<br>
 - docker run --privileged --rm -v $PWD/emulator/LOCAL/shared-storage:/home/submithost/emulator/LOCAL/shared-storage -p 9999:8888 submithostimage

## Run the Workflow

- When the docker run Sending DC_SET_READY message appears, open a web browser and enter the URL localhost:9999/apps/emulator.ipynb and enter the password emulator. This opens the emulator.ipynb Jupyter notebook in [Appmode](https://github.com/oschuett/appmode#). To open the emulator.ipynb Jupyter notebook in Edit Mode, enter the URL localhost:9999/notebooks/emulator.ipynb.
 
- The emulator.ipynb Jupyter Notebook provides the interface for running the workflow. Follow steps in emulator.ipynb to set up and run the workflow. 

- Setup includes volcano selection, material model and pile parameters for the volcano's eruption, parameters for the emulator's UQ software, VPC selection, as well as running a script that further configures the JSON-formatted information catalogs that Pegasus requires with your selected parameters.

- Logout of the emulator.ipynb Jupyter Notebook and enter Ctrl+C to stop the running Docker container.

## View Workflow Results

- Results and interim files generated for running a workflow are written to the mounted ./submithost/emulator/LOCAL/shared-storage directory.

- Results include the Hazard_Report.pdf file, which contains information on the probability of a volcanic flow depth reaching a critical height at specific locations. 

