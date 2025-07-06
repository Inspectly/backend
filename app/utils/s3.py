import os
from dotenv import load_dotenv

import boto3
from botocore.exceptions import ClientError

import aiobotocore.session

class S3:
    def __init__(self):
        load_dotenv(override = True)
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.s3_client_sync = boto3.client(
            's3',
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key
        )
        sts = boto3.client(
                'sts',
                aws_access_key_id = self.aws_access_key_id,
                aws_secret_access_key = self.aws_secret_access_key
            )
        self.session = aiobotocore.session.get_session()

    def get_buckets(self):
        try:
            response = self.s3_client.list_buckets()
            buckets = response['Buckets']
            return [bucket['Name'] for bucket in buckets]
        except ClientError as e:
            print(f'Error listing buckets: {e}')
            return []
        
    def get_bucket_objects(self, bucket_name, prefix = None):
        try:
            if prefix:
                response = self.s3_client.list_objects_v2(Bucket = bucket_name, Prefix = prefix)
            else:
                response = self.s3_client.list_objects_v2(Bucket = bucket_name)
            if ('Contents' in response):
                return [obj['Key'] for obj in response['Contents']]
            else:
                print(f'Bucket "{bucket_name}" is empty or does not exist')
                return []
        except ClientError as e:
            print(f'Error listing objects: {e}')
            return []
        
    def download_file(self, bucket_name, object_name, local_path):
        try:
            self.s3_client.download_file(bucket_name, object_name, local_path)
            return True
        except ClientError as e:
            print(f'Error downloading file: {e}')
            return False
        except FileNotFoundError:
            print(f'Local directory for {local_path} does not exist')
            return False
    
    def download_file_bytes(self, uri):
        try:
            bucket_name, object_name = uri.replace('s3://', '').split('/', 1)
            response = self.s3_client.get_object(Bucket = bucket_name, Key = object_name)
            file_content = response['Body'].read()
            return file_content
        except ClientError as e:
            print(f'Error downloading file as bytes: {e}')
            return None
        except Exception as e:
            print(f'Error downloading file as bytes: {e}')
            return None

    def upload_file(self, file_name, bucket_name, object_name = None):
        if object_name is None:
            object_name = os.path.basename(file_name)
        try:
            self.s3_client.upload_file(file_name, bucket_name, object_name)
            return f's3://{bucket_name}/{object_name}'
        except ClientError as e:
            print(f'Error uploading file: {e}')
            return False
        except FileNotFoundError:
            print(f'Local file {file_name} not found')
            return False
        
    async def upload_file_bytes(self, file, bucket_name, object_name):
        '''
        Uploads a file to S3.
        Args:
            file: The file to upload.
            bucket_name: The name of the bucket to upload the file to.
            object_name: The name of the object to upload the file to.
        Returns:
            True if the file was uploaded successfully, False otherwise.
        '''
        try:
            if object_name is None:
                object_name = file.filename

            file.file.seek(0)
            file_content = file.file.read()
            async with self.session.create_client(
                's3',
                region_name = 'us-east-2',
                aws_access_key_id = self.aws_access_key_id,
                aws_secret_access_key = self.aws_secret_access_key
            ) as s3_client:
                    await s3_client.put_object(
                    Bucket = bucket_name,
                    Key = object_name,
                    Body = file_content,
                    ContentType = file.content_type
                )
                    return f's3://{bucket_name}/{object_name}'
                        
        except Exception as e:
            print(f'Error checking bucket policy: {e}')
        
    def delete_file(self, bucket_name, object_name):
        try:
            self.s3_client.delete_object(Bucket = bucket_name, Key = object_name)
            return True
        except ClientError as e:
            print(f'Error deleting file: {e}')
            return False
        except Exception as e:
            print(f'Error deleting file: {e}')
            return False

if __name__ == '__main__':
    s3 = S3()
    print(s3.get_buckets())
    print(s3.get_bucket_objects('inspectly-ai-property-reports'))
    # print(s3.download_file_bytes('s3://test-bucket/test.txt'))
    # print(s3.upload_file('test.txt', 'test-bucket'))
    # print(s3.delete_file('test-bucket', 'test.txt'))
