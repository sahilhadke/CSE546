## CSE546_SahilYogeshHadke

##### ASU ID: 1229679960
##### ASURITE ID: shadke1

## Installation
```bash
pip install -r requirements.txt
```

## Run
```bash
python3 main.py
```

## Sample Output

```bash
===============
Launching EC2 instance...
Launched EC2 instance with ID: i-04362c5302b423fef
===============
===============
Creating SQS Queue...
SQS Queue created: test-queue-6890128.fifo
URL: https://sqs.us-east-1.amazonaws.com/654654563274/test-queue-6890128.fifo
===============
===============
Creating S3 bucket...
S3 Bucket created: test-bucket-6890128
===============
Waiting for 30 seconds...
===============
Listing Active EC2 Instances...
Instance ID: i-05ba8836d3cb78214 - terminated
Instance ID: i-0a8de9dbe86c6b21a - terminated
Instance ID: i-04362c5302b423fef - running
Instance ID: i-0f9b9448a42395f51 - terminated
Instance ID: i-0038a89e5379009fb - terminated
Instance ID: i-0f21b9ffbdcc09276 - terminated
===============
===============
Listing S3 Buckets...
- test-bucket-6890128
===============
===============
Listing SQS Queues...
SQS Queues:
- https://sqs.us-east-1.amazonaws.com/654654563274/test-queue-6890128.fifo
===============
===============
Uploading file to S3 bucket...
File ./CSE546test.txt uploaded to bucket test-bucket-6890128 as CSE546test.txt.
===============
===============
Sending message to SQS queue...
Message sent to SQS queue. Message ID: a41cc58a-9884-4a0c-a810-d38012a7d38c
===============
===============
Getting number of messages in SQS queue...
Number of messages in the queue: 1
===============
===============
Pulling messages from SQS queue...
Message Name: test message
Message Body: This is a test message
Message deleted from the queue.
No more messages in the queue.
===============
Waiting for 20 seconds...
===============
Getting number of messages in SQS queue...
Number of messages in the queue: 0
===============
===============
Terminating active EC2 instances...
Instance Terminated ID: ['i-04362c5302b423fef']
===============
===============
Deleting all S3 buckets...
Deleting all objects in bucket: test-bucket-6890128
Deleted object: CSE546test.txt
Deleted bucket: test-bucket-6890128
===============
===============
Deleting all SQS queues...
Deleting queue: https://sqs.us-east-1.amazonaws.com/654654563274/test-queue-6890128.fifo
Deleted queue: https://sqs.us-east-1.amazonaws.com/654654563274/test-queue-6890128.fifo
===============
Waiting for 60 seconds...
===============
Listing Active EC2 Instances...
Instance ID: i-05ba8836d3cb78214 - terminated
Instance ID: i-0a8de9dbe86c6b21a - terminated
Instance ID: i-04362c5302b423fef - terminated
Instance ID: i-0f9b9448a42395f51 - terminated
Instance ID: i-0038a89e5379009fb - terminated
Instance ID: i-0f21b9ffbdcc09276 - terminated
===============
===============
Listing S3 Buckets...
No S3 buckets found.
===============
===============
Listing SQS Queues...
No SQS queues found.
===============
```

