import boto3
from typing import BinaryIO


class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def get_url(self, bucket: str, filekey: str, bucket_location: dict[str, str]):
        return "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location["LocationConstraint"], bucket, filekey
        )

    def upload_file(self, file: BinaryIO, filename: str, id: str):
        bucket = "makym8545-bucket"
        filekey = f"shanyraks/{id}/{filename}"

        self.s3.upload_fileobj(file, bucket, filekey)

        bucket_location = boto3.client("s3").get_bucket_location(Bucket=bucket)

        return self.get_url(bucket, filekey, bucket_location)

    def delete_files(self, bucket, id: str):
        response = self.s3.list_objects_v2(Bucket=bucket)
        objects_to_delete = [
            obj["Key"] for obj in response["Contents"] if id in obj["Key"]
        ]
        if objects_to_delete:
            response = self.s3.delete_objects(
                Bucket=bucket,
                Delete={"Objects": [{"Key": key} for key in objects_to_delete]},
            )
            deleted_files = [obj["Key"] for obj in response.get("Deleted", [])]
            print("Deleted files:")
            for file in deleted_files:
                print(file)
        else:
            print("No files matching the substring were found.")
