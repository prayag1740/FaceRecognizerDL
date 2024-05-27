import boto3, time, os

pull_sqs_url = 'https://sqs.us-east-1.amazonaws.com/637423519415/1227975517-req-queue'
push_sqs_url = 'https://sqs.us-east-1.amazonaws.com/637423519415/1227975517-resp-queue'


class SQS:
    
    def __init__(self):
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        session_token = os.getenv('AWS_SESSION_TOKEN')
        self.sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1', aws_session_token=session_token)

    def send_request(self, request_id, response):

        message_attributes = {}
        message_attributes['request_id'] = {
            'DataType' : 'String',
            'StringValue' : request_id,
        }
        message_attributes['response'] = {
            'DataType' : 'String',
            'StringValue' : response
        }
        message_body=request_id
        
        response = self.sqs.send_message(QueueUrl=push_sqs_url, DelaySeconds=0, MessageAttributes=message_attributes, 
        MessageBody=message_body)

        return response


    def receive_request(self):

        start_time = time.time()

        response = self.sqs.receive_message(QueueUrl=pull_sqs_url, MessageAttributeNames=['All'], 
        VisibilityTimeout=0, WaitTimeSeconds=15)

        messages = response.get('Messages', [])

        if messages:
            msg = messages[0]
            end_time = time.time()
            time_diff = end_time - start_time
            print(f"Received msg after {time_diff} secs")
            self.sqs.delete_message(QueueUrl=pull_sqs_url, ReceiptHandle=msg['ReceiptHandle'])
            return msg

