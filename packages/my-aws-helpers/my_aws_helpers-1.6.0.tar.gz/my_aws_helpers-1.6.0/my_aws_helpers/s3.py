import boto3
import io
import json 
from typing import Tuple, Optional
from copy import copy
import os 
import gzip



class S3Location:
    bucket: str
    file_name: str
    location: str

    @classmethod
    def from_location(cls, location: str):
        bucket, file_name = location.split('/')[0], '/'.join(location.split('/')[1:])
        return cls(bucket = bucket, file_name = file_name)
    
    def __init__(self, bucket: str, file_name: str) -> None:
        self.bucket = bucket
        self.file_name = file_name
        self.location = f"{self.bucket}/{self.file_name}"

    def serialise(self):
        return copy(vars(self))
        

class S3:
    client: Optional[boto3.client]

    def __init__(self, client: Optional[boto3.client]) -> None:
        self.client = client if client else self._get_client()

    def _get_client(self) -> boto3.client:
        region_name = os.environ["AWS_DEFAULT_REGION"]
        s3_client = boto3.client("s3", region_name=region_name)
        endpoint_url = s3_client.meta.endpoint_url
        s3_client = boto3.client("s3", region_name=region_name, endpoint_url=endpoint_url)
        return s3_client

    def _streaming_body_to_dict(self, payload):
        file_like_obj = io.BytesIO(payload.read())
        response = json.loads(file_like_obj.getvalue())
        return response
    
    def put_json_object(self, bucket_name: str, file_name: str, object: dict):
        return self.client.put_object(
            Body = json.dumps(object),
            Bucket = bucket_name,
            Key = file_name
        )
    
    def get_object(self, bucket_name: str, file_name: str):
        response = self.client.get_object(
            Bucket = bucket_name,
            Key = file_name            
        )
        return self._streaming_body_to_dict(response["Body"])
    
    def get_presigned_url(self, bucket_name: str, file_name: str, expires_in: int = 3600):
        return self.client.generate_presigned_url(
            'get_object',
            Params = {
                "Bucket": bucket_name,
                "Key": file_name,
            },
            ExpiresIn = expires_in
        )
    
    def get_s3_location_from_bucket_file(bucket_name: str, file_name: str) -> S3Location:
        return S3Location(bucket=bucket_name, file_name=file_name)
    
    def get_bucket_file_from_s3_location(s3_location: S3Location) -> S3Location:
        return S3Location.from_location(location=s3_location)
    
    def save_document_content(
        self, 
        file_contents: bytes, 
        file_name: str, 
        bucket_name: str, 
        content_encoding: str = "", 
        content_type: str = "application/pdf",
        compress: bool = True,
    ) -> S3Location:
        """
        saves document content to bucket, in file_name
        Options for content_type: 
            "application/pdf"
            "text/plain"
            "application/json"
            probably more
        Options for content_encoding:
            "": default encoding
            "gzip": compressed contents
        """
        if compress or file_name.endswith(".gz"):
            file_contents = gzip.compress(file_contents)
            content_encoding = "gzip"
        obj = self.client.Object(bucket_name, file_name)
        obj.put(Body = file_contents, ContentType = content_type, ContentEncoding = content_encoding)
        return S3Location(bucket=bucket_name, file_name=file_name)
    
    def read_binary_from_s3(self, s3_location: S3Location) -> bytes:
        obj = self.client.Object(s3_location.bucket, s3_location.file_name)
        d_bytes = io.BytesIO()
        obj.download_fileobj(d_bytes)
        d_bytes.seek(0)
        if obj.content_encoding == "gzip":
            try:
                with gzip.GzipFile(fileobj=d_bytes) as gz_file:
                    return gz_file.read()
            except gzip.BadGzipFile:
                d_bytes.seek(0)
        return d_bytes.read()