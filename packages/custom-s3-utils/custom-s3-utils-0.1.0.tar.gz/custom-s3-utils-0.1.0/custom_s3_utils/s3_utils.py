import boto3
import uuid

class S3Utils:
    def __init__(self, bucket_name, region_name='us-east-1'):
        """
        Initialize the S3Utils class with bucket name and region.
        """
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name

    def upload_file(self, file_obj, key_prefix='', content_type=None):
        """
        Upload a file to S3.

        :param file_obj: File object to upload.
        :param key_prefix: Prefix for the file key in the bucket.
        :param content_type: Content type of the file.
        :return: Public URL of the uploaded file.
        """
        unique_filename = f"{uuid.uuid4()}_{file_obj.name}"
        key = f"{key_prefix}/{unique_filename}".lstrip('/')
        try:
            extra_args = {'ContentType': content_type} if content_type else {}
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                ExtraArgs=extra_args
            )
            return f"https://{self.bucket_name}.s3.amazonaws.com/{key}"
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to S3: {e}")