import os
import boto3
import re
import datetime
from zipfile37 import ZipFile
from botocore.exceptions import NoCredentialsError


def to_aws():
    ACCESS_KEY = 'AKIAYCZUHUEJ3LABHAV5'
    SECRET_KEY = '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'

    def upload_to_aws(local_file, bucket, ACCESS_KEY, SECRET_KEY):
        s3 = boto3.client('s3',aws_access_key_id = ACCESS_KEY,aws_secret_access_key= SECRET_KEY)

        try:
            s3.upload_file(local_file,bucket)
            print("success")
            return True
        except FileNotFoundError:
            print("No files with .bag exist in directory")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
    zipObj = ZipFile(datetime.datetime.now)
    for i in os.listdir('.'):
        match = re.search("\.bag$", i)
        if match: 
            zipObj.write(i)
    zipObj.close()
    upload_to_aws(zipObj,'vtanimanlsciencess3',ACCESS_KEY,SECRET_KEY)



