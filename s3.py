import os
import boto3


class S3:

    def __init__(self):
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    def download_file(self, bucket_name, key, path):
        self.s3.download_file(bucket_name, key, path)


    def delete_local_file(self, file_path):
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"success : deleted file --  {file_path}")
        else:
            print(f"fail : deleted file --  {file_path}")
