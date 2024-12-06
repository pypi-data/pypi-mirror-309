# custom_library.py
import boto3
from botocore.exceptions import ClientError
import uuid
from werkzeug.utils import secure_filename

class S3FileManager:
    def __init__(self, bucket_name, region):
        self.s3 = boto3.client('s3', region_name=region)
        self.bucket_name = bucket_name
        self.region = region

    def upload_file(self, file, filename, acl="public-read"):
        """Uploads a file to S3 and returns its URL if successful."""
        try:
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                filename,
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file.content_type
                }
            )
            file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{filename}"
            return file_url
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return None

    def delete_file(self, filename):
        """Deletes a file from S3 by filename."""
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=filename)
            return True
        except ClientError as e:
            print(f"Error deleting file: {e}")
            return False

class HelperFunctions:
    @staticmethod
    def allowed_file_extension(filename, allowed_extensions):
        """Checks if the file extension is allowed."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def generate_unique_id():
        """Generates a unique identifier using UUID."""
        return str(uuid.uuid4())

    @staticmethod
    def secure_filename_generator(filename):
        """Generates a secure filename for uploads."""
        return secure_filename(filename)
 