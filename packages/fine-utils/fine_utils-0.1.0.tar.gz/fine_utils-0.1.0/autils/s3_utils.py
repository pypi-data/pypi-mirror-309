import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import aioboto3
from botocore.exceptions import ClientError

from src.config.settings import settings


@dataclass
class S3Config:
    """S3配置"""

    bucket_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str = "ap-northeast-1"

    @classmethod
    def from_settings(cls, settings: "Settings") -> "S3Config":
        """从settings创建配置"""
        return cls(
            bucket_name=settings.aws.bucket_name,
            aws_access_key_id=settings.aws.access_key_id,
            aws_secret_access_key=settings.aws.secret_access_key,
            region_name=settings.aws.region,
        )


class AsyncS3Client:
    """异步S3客户端"""

    def __init__(self, config: S3Config):
        self.config = config
        self._session = aioboto3.Session(
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            region_name=config.region_name,
        )
        self._client = None

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self._client = await self._session.client("s3").__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def upload_file(
        self,
        file_path: str | Path,
        s3_key: str,
        extra_args: dict[str, Any] | None = None,
    ) -> str:
        """上传文件到S3"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not extra_args:
            extra_args = {}
            content_type, _ = mimetypes.guess_type(str(file_path))
            if content_type:
                extra_args["ContentType"] = content_type

        await self._client.upload_file(
            str(file_path), self.config.bucket_name, s3_key, ExtraArgs=extra_args
        )

        return f"https://{self.config.bucket_name}.s3.{self.config.region_name}.amazonaws.com/{s3_key}"

    async def download_file(self, s3_key: str, local_path: str | Path) -> Path:
        """从S3下载文件"""
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        await self._client.download_file(
            self.config.bucket_name, s3_key, str(local_path)
        )

        return local_path

    async def get_presigned_url(
        self, s3_key: str, expiration: int = 3600, http_method: str = "GET"
    ) -> str:
        """
        获取预签名URL
        :param s3_key: S3对象键
        :param expiration: 过期时间(秒)
        :param http_method: HTTP方法
        :return: 预签名URL
        """
        params = {"Bucket": self.config.bucket_name, "Key": s3_key}

        return await self._client.generate_presigned_url(
            f"{http_method.lower()}_object", Params=params, ExpiresIn=expiration
        )

    async def delete_file(self, s3_key: str) -> None:
        """删除S3文件"""
        await self._client.delete_object(Bucket=self.config.bucket_name, Key=s3_key)

    async def file_exists(self, s3_key: str) -> bool:
        """检查文件是否存在"""
        try:
            await self._client.head_object(Bucket=self.config.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise


# 使用示例
async def example_usage():
    config = S3Config.from_settings(settings)

    async with AsyncS3Client(config) as s3:
        # 上传文件并获取预签名URL
        private_key = "exlink/test/translations.json"
        private_key = "bc.html"
        await s3.upload_file(
            # "/Users/zhanghang/Documents/code/my/hashkey/exlink_new/data/trans/translations.json",
            "/Users/zhanghang/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/17dc1bf830ce821ab64175a817c669aa/Message/MessageTemp/21ade3b6e59686ba605988e098746d2a/File/bc.html",
            private_key,
        )
        url = await s3.get_presigned_url(private_key)
        print(url)


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_usage())
