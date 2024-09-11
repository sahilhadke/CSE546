import boto3
from dotenv import dotenv_values
import time

config = dotenv_values(".env")

# Configuration
ami_id = 'ami-0e86e20dae9224db8'
region = 'us-east-1'
aws_access_key = config['AWS_ACCESS_KEY']
aws_secret_access_key = config['AWS_SECRET_ACCESS_KEY']

# Initialize a session using your credentials
session = boto3.Session(
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_access_key,
    region_name = region
)

ec2 = session.resource('ec2')
ec2_client = session.client('ec2')
s3 = session.client('s3')
sqs = session.client('sqs')


# CREATE EC2 INSTANCE
def create_ec2_instance():
    instances = ec2.create_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='keypair_project1',
        SecurityGroupIds=['sg-04843879fa991460a'],
        SubnetId='subnet-03f060c757e868cbf',
    )
    for instance in instances:
        print(f'Launched EC2 instance with ID: {instance.id}')
    return instances[0].id


# CREATE S3 BUCKET
def create_s3_bucket(bucket_name):
    try:
        response = s3.create_bucket(
            Bucket=bucket_name
        )
        print(f'S3 Bucket created: {bucket_name}')
    except Exception as e:
        print(f'Error creating S3 bucket: {e}')

# CREATE SQS QUEUE
def create_sqs_queue(queue_name):
    try:
        # Create an SQS queue
        response = sqs.create_queue(
            QueueName=queue_name,
            Attributes={
                'DelaySeconds': '0',  # Default is no delay
                'MessageRetentionPeriod': '345600'  # Default is 4 days
            }
        )
        queue_url = response['QueueUrl']
        print(f'SQS Queue created: {queue_name}, URL: {queue_url}')
        return queue_url
    except Exception as e:
        print(f'Error creating SQS queue: {e}')

# LIST EC2 INSTANCES
def list_active_instances():
    try:
        response = ec2.instances.all()
        
        for instance in response:
            if instance.state['Name'] == 'running':
                print(f"Instance ID: {instance.id}")
                print(f"Instance Type: {instance.instance_type}")
                print(f"Public DNS: {instance.public_dns_name}")
                print(f"State: {instance.state['Name']}")
                print(f"Launch Time: {instance.launch_time}")
                print('-' * 60)
            # else:
            #     print("No active instances found.")
            #     return
    except Exception as e:
        print(f'Error retrieving instances: {e}')
# LIST S3 BUCKETS
def list_s3_buckets():
    try:
        # Retrieve the list of buckets
        response = s3.list_buckets()
        
        # Get the list of bucket names
        buckets = response.get('Buckets', [])
        
        # Check if there are any buckets
        if buckets:
            print("Active S3 Buckets:")
            for bucket in buckets:
                print(f"- {bucket['Name']}")
        else:
            print("No S3 buckets found.")
    except Exception as e:
        print(f'Error retrieving S3 buckets: {e}')

# LIST SQS QUEUES
def list_sqs_queues():
    try:
        # Retrieve the list of queues
        response = sqs.list_queues()
        
        # Get the list of queue URLs
        queue_urls = response.get('QueueUrls', [])
        
        # Check if there are any queues
        if queue_urls:
            print("SQS Queues:")
            for url in queue_urls:
                print(f"- {url}")
        else:
            print("No SQS queues found.")
    except Exception as e:
        print(f'Error retrieving SQS queues: {e}')


# UPLOAD TO S3 BUCKET
def upload_file_to_s3(file_path, bucket_name, object_key):
    try:
        # Upload the file
        s3.upload_file(file_path, bucket_name, object_key)
        print(f'File {file_path} uploaded to bucket {bucket_name} as {object_key}.')
    except Exception as e:
        print(f'Error uploading file: {e}')

# SEND MESSAGE TO SQS QUEUE
def send_message_to_sqs(queue_url, message_body, message_attribute_name):
    try:
        # Send the message
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes={
                'AttributeName': {
                    'StringValue': message_attribute_name,
                    'DataType': 'String'
                }
            }
        )
        print(f'Message sent to SQS queue. Message ID: {response["MessageId"]}')
    except Exception as e:
        print(f'Error sending message: {e}')



# CHECK MESSAGES IN SQS QUEUE
def receive_and_print_message(queue_url):
    while True:
        try:
            # Retrieve messages from the queue
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,  # Maximum number of messages to retrieve at once
                AttributeNames=['All'],  # Retrieve all attributes
                MessageAttributeNames=['All'],  # Retrieve all message attributes
                VisibilityTimeout=20,  # Time in seconds that the message is invisible after being retrieved
                WaitTimeSeconds=0  # Long polling wait time
            )
            
            # Extract messages
            messages = response.get('Messages', [])
            
            if not messages:
                print('No more messages in the queue.')
                break  # Exit the loop if no more messages
            
            # Process and delete each message
            for message in messages:
                message_id = message.get('MessageId', 'No ID')
                message_body = message.get('Body', 'No Body')
                receipt_handle = message.get('ReceiptHandle')
                
                print(f'Message ID: {message_id}')
                print(f'Message Body: {message_body}')
                
                # Delete the message from the queue after processing
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
                print('Message deleted from the queue.')
            
            # Optional: Sleep to avoid hitting API rate limits
            time.sleep(1)
        
        except Exception as e:
            print(f'Error retrieving or deleting messages: {e}')
            break

# TERMINATE ACTIVE EC2 INSTANCES
def terminate_active_instances():
    try:
        response = ec2_client.describe_instances()
        
        instances_to_terminate = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] == 'running':
                    instances_to_terminate.append(instance['InstanceId'])
        
        if instances_to_terminate:
            print(f"Terminating instances: {instances_to_terminate}")
            terminate_response = ec2_client.terminate_instances(InstanceIds=instances_to_terminate)
            print("Termination response:", terminate_response)
        else:
            print("No running instances found.")
    except Exception as e:
        print(f'Error terminating instances: {e}')


# TERMINATE S3 BUCKETS
def delete_all_buckets():
    try:
        # List all buckets
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        
        if not buckets:
            print('No S3 buckets found.')
            return
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            print(f'Deleting all objects in bucket: {bucket_name}')
            
            # List and delete all objects in the bucket
            objects = s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
            
            if objects:
                for obj in objects:
                    s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                    print(f'Deleted object: {obj["Key"]}')
            
            # Delete the bucket
            s3.delete_bucket(Bucket=bucket_name)
            print(f'Deleted bucket: {bucket_name}')
    
    except Exception as e:
        print(f'Error deleting buckets: {e}')

# TERMINATE SQS QUEUES
def delete_all_queues():
    try:
        # List all queues
        response = sqs.list_queues()
        queue_urls = response.get('QueueUrls', [])
        
        if not queue_urls:
            print('No SQS queues found.')
            return
        
        for queue_url in queue_urls:
            print(f'Deleting queue: {queue_url}')
            sqs.delete_queue(QueueUrl=queue_url)
            print(f'Deleted queue: {queue_url}')
    
    except Exception as e:
        print(f'Error deleting queues: {e}')

create_ec2_instance()
create_s3_bucket('test-bucket-1239101231923130')
queue_url = create_sqs_queue('test-queue-1239101231923130')

print('Waiting for 60 seconds...')
time.sleep(60)

list_active_instances()
list_s3_buckets()
list_sqs_queues()

upload_file_to_s3('./CSE546test.txt', 'test-bucket-1239101231923130', 'CSE546test.txt')
send_message_to_sqs(queue_url, 'This is a test message', 'test message')
receive_and_print_message(queue_url)

print('Waiting for 30 seconds...')
time.sleep(30)

terminate_active_instances()
delete_all_buckets()
delete_all_queues()

list_active_instances()
list_s3_buckets()
list_sqs_queues()