import os
import boto3, uuid
from face_recognition import face_match
from s3 import S3
from sqs import SQS

def main():

    sqs = SQS()
    s3 = S3()
    while True:
        sqs_message = sqs.receive_request()
        if not sqs_message:
            continue

        request_id = sqs_message['MessageAttributes']['request_id']['StringValue']
        bucket_name = sqs_message['MessageAttributes']['bucket_name']['StringValue']
        key = sqs_message['MessageAttributes']['key']['StringValue']

        print("APP TIER: Starting face reognition for request ID --- " + request_id)
        
        current_path = os.getcwd()
        file_path_local = current_path + "/" + key
        
        s3.download_file(bucket_name, key, file_path_local)

        print("APP TIER: downloaded file from S3 input bucket")

        result = face_match(file_path_local, 'data.pt')
        
        sqs.send_request(request_id, result[0])
        print("APP TIER: sent response to response SQS queue")
        
        s3.delete_local_file(file_path_local)
        

        
        
if __name__ == "__main__":
    main()