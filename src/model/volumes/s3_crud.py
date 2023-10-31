import os
import shutil
from boto3.s3.transfer import S3Transfer

class s3_crud:
    @staticmethod
    def upload_to_s3(bucket_name, source_directory, target_directory, s3):
        transfer = S3Transfer(s3)
        for root, _, filenames in os.walk(source_directory):
            for filename in filenames:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, source_directory)
                s3_path = os.path.join(target_directory, relative_path)
                if filename.endswith('.css'):
                    transfer.upload_file(local_path, bucket_name, s3_path, extra_args={'ContentType': 'text/css'})
                else:
                    transfer.upload_file(local_path, bucket_name, s3_path)

        shutil.rmtree(source_directory)
        print(f'{source_directory} Uploaded Successfully')
