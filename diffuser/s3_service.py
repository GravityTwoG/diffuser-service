import io
import json
import boto3
from botocore.exceptions import ClientError

class S3Service:

  def __init__(
    self, 
    bucket_name: str, 
    endpoint: str, 
    access_key: str, 
    secret_key: str,
  ):
    self.bucket_name = bucket_name
    self.s3 = boto3.client('s3',
      endpoint_url=endpoint,
      aws_session_token=None,
      aws_access_key_id=access_key,
      aws_secret_access_key=secret_key,
    )

    self.verify_bucket()


  def verify_bucket(self):
    try:
      # check if bucket exists
      self.s3.head_bucket(Bucket=self.bucket_name)
    
    except self.s3.exceptions.NoSuchBucket:
      self.s3.create_bucket(Bucket=self.bucket_name)
      self.set_read_only_policy()

    except ClientError as e:
      error_code = e.response['Error']['Code']
      if error_code == '403':
        raise Exception(f"Do not have permission to access bucket {self.bucket_name}.")
      else:
          raise


  def set_read_only_policy(self):
    policy = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "PublicRead",
          "Effect": "Allow",
          "Principal": "*",
          "Action": ["s3:GetObject", "s3:ListBucket"],
          "Resource": [
            f"arn:aws:s3:::{self.bucket_name}",
            f"arn:aws:s3:::{self.bucket_name}/*"
          ]
        }
      ]
    }
    self.set_bucket_policy(policy)


  def set_bucket_policy(self, policy):
    try:
      self.s3_client.put_bucket_policy(Bucket=self.bucket_name, Policy=json.dumps(policy))
      print(f"Successfully set policy for bucket {self.bucket_name}")
    except ClientError as e:
      print(f"Error setting bucket policy: {str(e)}")



  def save_images(self, images: list):
    for image in images:
      image_name = image['image_name']
      image = image['image']
      
      # Convert image to bytes
      img_byte_arr = io.BytesIO()
      image.save(img_byte_arr, format='PNG')
      img_byte_arr.seek(0)  # Reset file pointer to the beginning

      # Upload to S3
      self.s3.upload_fileobj(
        img_byte_arr,
        self.bucket_name,
        image_name,
        ExtraArgs={
          'ContentType': 'image/png'
        }
      )
  
