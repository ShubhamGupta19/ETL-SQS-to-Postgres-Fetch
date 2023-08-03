import json
import boto3
import os

os.environ["AWS_ACCESS_KEY_ID"] = "dummy_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "dummy_secret_key"

def read_data_from_sqs(queue_name):
    try:
        sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
        response = sqs.receive_message(
            QueueUrl='http://localhost:4566/000000000000/login-queue',
            MaxNumberOfMessages=10,
            VisibilityTimeout=30,
            WaitTimeSeconds=20
        )

        messages = response.get('Messages', [])
        data = []
        for message in messages:
            data.append(json.loads(message['Body']))
            # Delete the processed message from the SQS queue
            sqs.delete_message(QueueUrl='http://localhost:4566/000000000000/login-queue', ReceiptHandle=message['ReceiptHandle'])

        return data

    except Exception as e:
        raise Exception(f"Error while reading from SQS: {str(e)}")