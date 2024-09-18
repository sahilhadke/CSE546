## Summary
In the first project, we will build an application that can communicate with IaaS service online and request certain resources from the IaaS provider. Specifically, we will build this application using the Amazon Web Services (AWS) SDK and API. AWS is the most widely used IaaS provider and offers a variety of computing, storage, and messaging services. The technologies and techniques that we learn during this project will be useful for us to build others in the future.

## Description
*(This is an individual project.)*
You need to program an application that requests a list of required resources from AWS, check and list all the resources assigned to you, then destroy all the resources.

### The required resources are:
- An EC2 instance(VM): Using free tier eligable Ubuntu AMIT2.micro tier
- Using your own key pair with your name as the key pair name
- An S3 bucket.
- An SQS queue with the FIFO type.
### Your application should:
- Load the AWS SDK(you may use whatever language you prefer, as long as there is an AWS SDK available)
- Read your access information, to be able to access AWS service (Guidance of how to get access information like access key ID, token and session key are included in the AWS Introduction ppt that was shared with you earlier.)
- Send resource request API call to AWS to create the EC2 instance, S3 bucket, and SQS queue.
- Wait for 1 min.
- List all EC2 instances, S3 buckets, and SQS queues in your accounts in the current region again, print them out.
- Upload an empty text file with the name “CSE546test.txt” into the S3 bucket that you just created.
- Send a message with the message name “test message” and message body “This is a test message” into the SQS queue.
- Check how many messages are there in your SQS queue, print it out in a new line.
- Pull the message you just sent from the SQS queue, print out the message name and body in two lines.
- Check how many messages are there in your SQS queue again.
- Wait for 10 seconds.
- Delete all the resources.
- Wait for 20 seconds.
- List all EC2 instances, S3 buckets, and SQS queues in your accounts in the current region again.
- Also, print out a message each time an action is done. For example, when you sent all the resource requests and start to wait for 1 minute, you should print out “Request sent, wait for 1 min”. Another example, after you sent the message to SQS queue, you should print out a new line: “Message sent”. And so on.

### Test your code thoroughly. Check the following:
- All the resources are correctly created, 1 minute should be more than enough for AWS to create them, you may increase the waiting time during your test;
- The file is uploaded to S3 bucket;
- SQS queue received your message, stored and sent it.

Your project will be graded according to the above criteria.