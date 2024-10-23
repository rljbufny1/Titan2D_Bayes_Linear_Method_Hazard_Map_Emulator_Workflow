import boto3
import time

def pegasus_aws_batch_delete(prefix):

    print ('pegasus_aws_batch_delete...')
    print ('prefix: ', prefix)

    # Create the boto3 clients
    boto3_ecs_client = boto3.client('ecs')
    boto3_batch_client = boto3.client('batch')

    print ('Disable and delete the %s-job-queue job queue...' %prefix)
    try:
        response = boto3_batch_client.update_job_queue(jobQueue='%s-job-queue' %prefix, state='DISABLED')
    except Exception as e:
        print ("pegasus_aws_batch_delete update_job_queue Exception: %s\n" %str(e))
        
    # Wait up to 2 minutes for the state to change.
    # See https://ec2spotworkshops.com/rendering-with-batch/cleanup.html
    wait_interval = 5
    wait_loops = int(120/wait_interval)
    try:
        wait_time = 0
        for i in range(wait_loops):
            time.sleep(wait_interval)
            wait_time = wait_time + wait_interval
            response = boto3_batch_client.describe_job_queues(jobQueues=['%s-job-queue' %prefix])
            if not response['jobQueues'] or (response['jobQueues'][0]['state'] == 'DISABLED' and response['jobQueues'][0]['status'] == 'VALID'):
                print ('update_job_queue wait time: ', wait_time, ' [sec]')
                break
    except Exception as e:
        print ("pegasus_aws_batch_delete describe_job_queues Exception: %s\n" %str(e))
    
    try:
        response = boto3_batch_client.delete_job_queue(jobQueue='%s-job-queue' %prefix)
    except Exception as e:
        print ("pegasus_aws_batch_delete delete_job_queue Exception: %s\n" %str(e))
    
    try:
        wait_time = 0
        for i in range(wait_loops):
            time.sleep(wait_interval)
            wait_time = wait_time + wait_interval
            response = boto3_batch_client.describe_job_queues(jobQueues=['%s-job-queue' %prefix])
            if not response['jobQueues'] or response['jobQueues'][0]['status'] == 'DELETED':
               print ('delete_job_queue wait time: ', wait_time, ' [sec]')
               break
    except Exception as e:
        print ("pegasus_aws_batch_delete describe_job_queues Exception: %s\n" %str(e))
        
    print ('Disable and delete the %s-compute-env compute environment...' %prefix)
    try:
        response = boto3_batch_client.update_compute_environment(computeEnvironment='%s-compute-env' %prefix, state='DISABLED')
    except Exception as e:
        print ("pegasus_aws_batch_delete update_compute_environment Exception: %s\n" %str(e))
    
    try:
        wait_time = 0
        for i in range(wait_loops):
            time.sleep(wait_interval)
            wait_time = wait_time + wait_interval
            response = boto3_batch_client.describe_compute_environments(computeEnvironments=['%s-compute-env' %prefix])
            if not response['computeEnvironments'] or (response['computeEnvironments'][0]['state'] == 'DISABLED' and response['computeEnvironments'][0]['status'] == 'VALID'):
                print ('update_compute_environment wait time: ', wait_time, ' [sec]')
                break
    except Exception as e:
        print ("pegasus_aws_batch_delete describe_compute_environments: %s\n" %str(e))
    
    try:
        response = boto3_batch_client.delete_compute_environment(computeEnvironment='%s-compute-env' %prefix)
    except Exception as e:
        print ("pegasus_aws_batch_delete delete_compute_environment Exception: %s\n" %str(e))

    try:
        wait_time = 0
        for i in range(wait_loops):
            time.sleep(wait_interval)
            wait_time = wait_time + wait_interval
            response = boto3_batch_client.describe_compute_environments(computeEnvironments=['%s-compute-env' %prefix])
            if not response['computeEnvironments'] or response['computeEnvironments'][0]['status'] == 'DELETED':
                print ('delete_compute_environment wait time: ', wait_time, ' [sec]')
                break
    except Exception as e:
        print ("pegasus_aws_batch_delete describe_compute_environments: %s\n" %str(e))
        
    print ('Deregister %s-job-definition...' %prefix)
    # Note: job definitions can be deregistered but not deleted.
    # Deregistered job definitions are deleted after 180 days, see https://docs.aws.amazon.com/batch/latest/APIReference/API_DeregisterJobDefinition.html.
    try:
        response = boto3_batch_client.deregister_job_definition(jobDefinition='%s-job-definition:1' %prefix)
    except Exception as e:
        print ("pegasus_aws_batch_delete deregister_job_definition Exception: %s\n" %str(e))

    try:
        wait_time = 0
        for i in range(wait_loops):
            time.sleep(wait_interval)
            wait_time = wait_time + wait_interval
            response = boto3_batch_client.describe_job_definitions(jobDefinitions=['%s-job-definition:1' %prefix])
            if not response['jobDefinitions'] or response['jobDefinitions'][0]['status'] == 'INACTIVE':
                print ('deregister_job_definition wait time: ', wait_time, ' [sec]')
                break
    except Exception as e:
        print ("pegasus_aws_batch_delete describe_job_definitions: %s\n" %str(e))
