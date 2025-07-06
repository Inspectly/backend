from app.utils.s3 import S3
from app.schema.properties import Reports
from app.utils.helpers import get_file_unique_name

class AWS_Operations:
    def __init__(self):
        self.s3 = S3()

    async def upload_file(self, user_id: int, listing_id: int, name: str, property_report):
        return await self.s3.upload_file_bytes(property_report, 'inspectly-ai-property-reports', get_file_unique_name(user_id, listing_id, name))
    
    async def download_file(self, bucket_name, object_name):
        return self.s3.download_file(bucket_name, object_name)
