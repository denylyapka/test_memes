from contextlib import asynccontextmanager

from aiobotocore.session import get_session

import os
from dotenv import load_dotenv

load_dotenv()

access_key_env = os.getenv('access_key')
secret_key_env = os.getenv('secret_key')
endpoint_url_env = os.getenv('endpoint_url')
bucket_name_env = os.getenv('bucket_name')


s3_base_link = os.getenv('s3_base_link')


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_path: str):
        object_name = file_path.split("/")[-1]
        async with self.get_client() as client:
            with open(file_path, 'rb') as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file
                )
        return object_name

    async def remove_file(self, file_path: str):
        object_name = file_path.split("/")[-1]
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=object_name)


async def get_name_and_file_upload(file_path):
    s3_client = S3Client(
        access_key=access_key_env,
        secret_key=secret_key_env,
        endpoint_url=endpoint_url_env,
        bucket_name=bucket_name_env
    )
    # print(s3_base_link + file_path)  # Выводит ссылку на фото
    await s3_client.upload_file(file_path)


async def get_name_and_file_remove(file_path):
    s3_client = S3Client(
        access_key=access_key_env,
        secret_key=secret_key_env,
        endpoint_url=endpoint_url_env,
        bucket_name=bucket_name_env
    )
    await s3_client.remove_file(file_path)