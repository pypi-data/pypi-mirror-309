import boto3

from dataclasses import dataclass
from typing import Optional


def remove_none_values(data: dict) -> dict:  # noqa: WPS110
    return {key: value for key, value in data.items() if value is not None}  # noqa: WPS110


@dataclass
class S3Bucket(object):
    bucket_name: str

    def __post_init__(self):
        self._resource = boto3.resource('s3')

    def get(self, file_key: str) -> Optional[dict]:
        try:
            return self._resource.Object(self.bucket_name, file_key).get()
        except self._resource.meta.client.exceptions.NoSuchKey:
            return None

    def get_bytes(self, file_key: str) -> Optional[bytes]:
        file_context = self.get(file_key)
        if not file_context:
            return None
        return (
            file_context['Body'].read()
            if 'Body' in file_context
            else None
        )

    def upload(self, file_key: str, file_content, content_type: Optional[str] = None):
        optional_params = {'ContentType': content_type}
        return self._resource.Object(self.bucket_name, file_key).put(
            Body=file_content,
            **remove_none_values(optional_params),
        )

    def delete(self, file_key: str):
        return self._resource.Object(self.bucket_name, file_key).delete()

    def get_url(self, file_key: str):
        return 'https://{bucket_url}.s3.amazonaws.com/{file_key}'.format(
            bucket_url=self.bucket_name,
            file_key=file_key,
        )

    def read(self, file_key: str) -> bytes:
        return self.get(file_key)['Body'].read()
