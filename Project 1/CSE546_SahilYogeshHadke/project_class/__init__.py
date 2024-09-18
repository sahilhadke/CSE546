import boto3
import time
import random
import hashlib

class cloud_project_one:

    def __init__(self, aws_access_key, aws_secret_access_key, region, queue_name, bucket_name):

        # Initialize a session using your credentials
        session = boto3.Session(
            aws_access_key_id = aws_access_key,
            aws_secret_access_key = aws_secret_access_key,
            region_name = region
        )

        self.ec2 = session.resource('ec2')
        self.ec2_client = session.client('ec2')
        self.s3 = session.client('s3')
        self.sqs = session.client('sqs')
        self.random_id = random.randint(1, 1000)
        self.queue_name = queue_name
        self.s3_bucket_name = bucket_name

    # CREATE RESOURCES 
    def create_instance(self):
        print('='*15)
        print('Launching EC2 instance...')
        instances = self.ec2.create_instances(
            ImageId='ami-0ac019f4fcb7cb7e6',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='keypair_project1',
            SecurityGroupIds=['sg-04843879fa991460a'],
            SubnetId='subnet-03f060c757e868cbf',
        )
        for instance in instances:
            print(f'Launched EC2 instance with ID: {instance.id}')

            print('='*15)
        return instances[0].id

    def create_sqs_queue(self):
        print('='*15)
        print('Creating SQS Queue...')
        try:
            # Create an SQS queue
            response = self.sqs.create_queue(
                QueueName=self.queue_name,
                Attributes={
                    'DelaySeconds': '0',  # Default is no delay
                    'MessageRetentionPeriod': '345600',  # Default is 4 days
                    'FifoQueue': 'true'
                }
            )
            queue_url = response['QueueUrl']
            print(f'SQS Queue created: {self.queue_name}')
            print(f'URL: {queue_url}')
            print('='*15)
            return queue_url
        except Exception as e:
            print(f'Error creating SQS queue: {e}')

    def create_bucket(self):
        print('='*15)
        print('Creating S3 bucket...')
        try:
            response = self.s3.create_bucket(
                Bucket=self.s3_bucket_name
            )
            print(f'S3 Bucket created: {self.s3_bucket_name}')
            print('='*15)
        except Exception as e:
            print(f'Error creating S3 bucket: {e}')

    # DELETE RESOURCES
    def delete_bucket(self):
        print('='*15)
        print('Deleting all S3 buckets...')
        try:
            # List all buckets
            response = self.s3.list_buckets()
            buckets = response.get('Buckets', [])
            
            if not buckets:
                print('No S3 buckets found.')
                return
            
            for bucket in buckets:
                bucket_name = bucket['Name']
                print(f'Deleting all objects in bucket: {bucket_name}')
                
                # List and delete all objects in the bucket
                objects = self.s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
                
                if objects:
                    for obj in objects:
                        self.s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                        print(f'Deleted object: {obj["Key"]}')
                
                # Delete the bucket
                self.s3.delete_bucket(Bucket=bucket_name)
                print(f'Deleted bucket: {bucket_name}')
        
        except Exception as e:
            print(f'Error deleting buckets: {e}')

        print('='*15)
    def delete_sqs_queues(self):
        print('='*15)
        print('Deleting all SQS queues...')
        try:
            # List all queues
            response = self.sqs.list_queues()
            queue_urls = response.get('QueueUrls', [])
            
            if not queue_urls:
                print('No SQS queues found.')
                return
            
            for queue_url in queue_urls:
                print(f'Deleting queue: {queue_url}')
                self.sqs.delete_queue(QueueUrl=queue_url)
                print(f'Deleted queue: {queue_url}')
        except Exception as e:
            print(f'Error deleting queues: {e}')

        print('='*15)

    def terminate_instances(self):
        print('='*15)
        print('Terminating active EC2 instances...')
        try:
            response = self.ec2_client.describe_instances()
            
            instances_to_terminate = []
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        instances_to_terminate.append(instance['InstanceId'])
            
            if instances_to_terminate: 
                terminate_response = self.ec2_client.terminate_instances(InstanceIds=instances_to_terminate)

                print(f"Instance Terminated ID: {instances_to_terminate}")
            else:
                print("No running instances found.")
        except Exception as e:
            print(f'Error terminating instances: {e}')

        print('='*15)

    # LIST RESOURCES
    def list_buckets(self):
        print('='*15)
        print('Listing S3 Buckets...')
        try:
            # Retrieve the list of buckets
            response = self.s3.list_buckets()
            
            # Get the list of bucket names
            buckets = response.get('Buckets', [])
            
            # Check if there are any buckets
            if buckets:
                for bucket in buckets:
                    print(f"- {bucket['Name']}")
            else:
                print("No S3 buckets found.")
        
        except Exception as e:
            print(f'Error retrieving S3 buckets: {e}')


        print('='*15)

    def list_instances(self):
        print('='*15)
        print('Listing Active EC2 Instances...')
        try:
            response = self.ec2.instances.all()

            running_instance_count = 0
            
            for instance in response:
                print(f"Instance ID: {instance.id} - {instance.state['Name']}")
                running_instance_count += 1
        except Exception as e:
            print(f'Error retrieving instances: {e}')

        if running_instance_count == 0:
            print('No running instances found.')
        
        print('='*15)

    def list_sqs_queues(self):

        print('='*15)
        print('Listing SQS Queues...')
        try:
            # Retrieve the list of queues
            response = self.sqs.list_queues()
            
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

        print('='*15)


    # UPLOAD FILE TO S3
    def upload_file(self, file_path,bucket_name, object_key):
        print('='*15)
        print('Uploading file to S3 bucket...')
        try:
            # Upload the file
            self.s3.upload_file(file_path, bucket_name, object_key)
            print(f'File {file_path} uploaded to bucket {bucket_name} as {object_key}.')
        except Exception as e:
            print(f'Error uploading file: {e}')
        
        print('='*15)

    # SEND MESSAGE TO SQS
    

    def send_message(self, queue_url, message_body, message_attribute_name, message_group_id="MessageGroup1"):
        if not queue_url:
            print('Error: QueueUrl is None or empty.')
            return

        print('='*15)
        print('Sending message to SQS queue...')
        try:
            # Generate a deduplication ID based on the message body
            message_deduplication_id = hashlib.md5(message_body.encode('utf-8')).hexdigest()

            # Send the message
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message_body,
                MessageAttributes={
                    'AttributeName': {
                        'StringValue': message_attribute_name,
                        'DataType': 'String'
                    }
                },
                MessageGroupId=message_group_id,  # Add MessageGroupId for FIFO queues
                MessageDeduplicationId=message_deduplication_id  # Add MessageDeduplicationId
            )
            print(f'Message sent to SQS queue. Message ID: {response["MessageId"]}')
        except Exception as e:
            print(f'Error sending message: {e}')

        print('='*15)

    # GET NUMBER OF MESSAGES IN SQS
    def get_number_of_messages(self, queue_url):
        print('='*15)
        print('Getting number of messages in SQS queue...')
        try:
            # Get the queue attributes
            response = self.sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['ApproximateNumberOfMessages']
            )
            num_messages = response['Attributes']['ApproximateNumberOfMessages']
            print(f'Number of messages in the queue: {num_messages}')
        except Exception as e:
            print(f'Error getting number of messages: {e}')

        print('='*15)

    # RECEIVE MESSAGE FROM SQS
    def receive_and_print_message(self, queue_url):

        print('='*15)
        print('Pulling messages from SQS queue...')

        while True:
            try:
                # Retrieve messages from the queue
                response = self.sqs.receive_message(
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
                    self.sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=receipt_handle
                    )
                    print('Message deleted from the queue.')
                
                # Optional: Sleep to avoid hitting API rate limits
                time.sleep(1)
            
            except Exception as e:
                print(f'Error retrieving or deleting messages: {e}')
                break
        
        print('='*15)