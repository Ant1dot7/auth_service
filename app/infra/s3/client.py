from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import BinaryIO

from aiobotocore.session import get_session


@dataclass(eq=False)
class S3Client:
    aws_access_key_id: str
    aws_secret_access_key: str
    endpoint_url: str

    def __post_init__(self):
        self.session = get_session()
        self._config = {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "endpoint_url": self.endpoint_url,
        }

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self._config) as client:
            yield client

    async def upload_file_bytes(
            self,
            bucket_name: str,
            file_bytes: bytes | BinaryIO,
            s3_path: str,
    ) -> None:
        async with self.get_client() as client:
            await client.put_object(
                Bucket=bucket_name,
                Key=s3_path,
                Body=file_bytes,
            )
    # def download_file(self, file_path: str, s3_path: str):
    #     try:
    #         self.client.download_file(self.bucket_name, s3_path, file_path)
    #     except ClientError:
    #         print(f"Файл {s3_path} не найден.")
