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
Launched EC2 instance with ID: i-0a8de9dbe86c6b21a
===============
===============
Creating SQS Queue...
SQS Queue created: test-queue-6389706.fifo
URL: https://sqs.us-east-1.amazonaws.com/654654563274/test-queue-6389706.fifo
===============
===============
Creating S3 bucket...
S3 Bucket created: test-bucket-6389706
===============
Waiting for 30 seconds...
===============
Listing Active EC2 Instances...
Instance ID: i-0a8de9dbe86c6b21a - running
===============
===============
Listing S3 Buckets...
- test-bucket-6389706
===============
===============
Listing SQS Queues...
SQS Queues:
- https://sqs.us-east-1.amazonaws.com/654654563274/test-queue-6389706.fifo
===============
===============
Uploading file to S3 bucket...
File ./CSE546test.txt uploaded to bucket test-bucket-6389706 as CSE546test.txt.
===============
===============
Sending message to SQS queue...
Message sent to SQS queue. Message ID: 9b1dd0c1-5916-4f0a-b8d3-cd1864a66dc1
===============
===============
Getting number of messages in SQS queue...
Number of messages in the queue: 1
===============
===============
Pulling messages from SQS queue...
Message ID: 9b1dd0c1-5916-4f0a-b8d3-cd1864a66dc1
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
Instance Terminated ID: ['i-0a8de9dbe86c6b21a']
===============
===============
Deleting all S3 buckets...
Deleting all objects in bucket: test-bucket-6389706
Deleted object: CSE546test.txt
Deleted bucket: test-bucket-6389706
===============
===============
Deleting all SQS queues...
Deleting queue: https://sqs.us-east-1.amazonaws.com/654654563274/test-queue-6389706.fifo
Deleted queue: https://sqs.us-east-1.amazonaws.com/654654563274/test-queue-6389706.fifo
===============
Waiting for 60 seconds...
===============
Listing Active EC2 Instances...
Instance ID: i-0a8de9dbe86c6b21a - terminated
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

