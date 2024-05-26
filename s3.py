import os
import boto3


class S3:

    def __init__(self, credentials):
        aws_access_key_id = credentials['AccessKeyId']
        aws_secret_access_key = credentials['SecretAccessKey']
        session_token = credentials['SessionToken']
        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1', aws_session_token=session_token)

    def download_file(self, bucket_name, key, path):
        self.s3.download_file(bucket_name, key, path)


    def delete_local_file(self, file_path):
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"success : deleted file --  {file_path}")
        else:
            print(f"fail : deleted file --  {file_path}")
