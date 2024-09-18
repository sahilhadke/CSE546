from dotenv import dotenv_values
import time
import random
from project_class import cloud_project_one 

config = dotenv_values(".env")

# Configuration
ami_id = 'ami-0e86e20dae9224db8'
region = 'us-east-1'
aws_access_key = config['AWS_ACCESS_KEY']
aws_secret_access_key = config['AWS_SECRET_ACCESS_KEY']
random_number = random.randrange(1000000, 9999999)
s3_bucket_name = f'test-bucket-{random_number}'
sqs_queue_name = f'test-queue-{random_number}.fifo'

cloud_project = cloud_project_one(aws_access_key, aws_secret_access_key, region, sqs_queue_name, s3_bucket_name)

cloud_project.create_instance()
queue_url = cloud_project.create_sqs_queue()
cloud_project.create_bucket()

print('Waiting for 30 seconds...')
time.sleep(30)

cloud_project.list_instances()
cloud_project.list_buckets()
cloud_project.list_sqs_queues()

cloud_project.upload_file('./CSE546test.txt', s3_bucket_name, 'CSE546test.txt')
cloud_project.send_message(queue_url, 'This is a test message', 'test message')
cloud_project.get_number_of_messages(queue_url)
cloud_project.receive_and_print_message(queue_url)

print('Waiting for 20 seconds...')
time.sleep(20)

cloud_project.get_number_of_messages(queue_url)
cloud_project.terminate_instances()
cloud_project.delete_bucket()
cloud_project.delete_sqs_queues()

print('Waiting for 60 seconds...')
time.sleep(60)

cloud_project.list_instances()
cloud_project.list_buckets()
cloud_project.list_sqs_queues()
