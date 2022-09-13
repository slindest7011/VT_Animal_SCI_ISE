import os
import boto3
import re
import datetime
from zipfile37 import ZipFile
from botocore.exceptions import NoCredentialsError
import rosbag


import subprocess
import yaml
import cv2
from cv_bridge import CvBridge
import numpy as np
import time
import argparse
import sensor_msgs.msg


def to_aws(number_or_image):
    ACCESS_KEY = ''
    SECRET_KEY = ''

    def upload_to_aws(local_file, bucket, ACCESS_KEY, SECRET_KEY):
        s3 = boto3.client('s3',aws_access_key_id = ACCESS_KEY,aws_secret_access_key= SECRET_KEY)

        try:
            s3.upload_file(local_file,bucket, number_or_image +'/' + str(datetime.date.today())+'.zip')
            print("success")
            return True
        except FileNotFoundError:
            print("No files with .zip exist in directory")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    local_file_name = str(datetime.date.today()) +'.zip'
    with ZipFile(local_file_name, 'w') as zipObj:
        for i in os.listdir('.'):
            match = re.search("\.bag$", i)
            if match:
                print(i)
                try:
                    zipObj.write(str(i))
                #assert os.path.isfile(i)
                except PermissionError:
                    break

    upload_to_aws(local_file_name,'vtanimanlsciencess3',ACCESS_KEY,SECRET_KEY)


import boto3
import re
import json
import numpy as np
# All of this is subject to change with the contigency of different naming conventions

def lambda_handler():
    # initalize services used
    ACCESS_KEY = 'AKIAYCZUHUEJ3LABHAV5'
    SECRET_KEY = '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'

    s3_client = boto3.client('s3',aws_access_key_id = ACCESS_KEY,aws_secret_access_key= SECRET_KEY)
    s3_resource = boto3.resource("s3", aws_access_key_id = ACCESS_KEY,aws_secret_access_key= SECRET_KEY)
    unzip_lambda_client = boto3.client("lambda",'us-east-1') # will be used to unzip sent directories
    
    #Defining directories that exist in
    my_bucket = s3_resource.Bucket('vtanimanlsciencess3')
    image_files =list(my_bucket.objects.filter(Prefix='image/'))[1:]#directory for cow images
    number_files = list(my_bucket.objects.filter(Prefix='number/'))[1:]#directory for number images
    
    print("This is the image/ and number/ directories")
    print(image_files)
    print(number_files)
    
    
    
    # This is used to search for the zip file in the two directories
    def zip_search(file_path):
        zip_files =[]
        for file in file_path:
            match = re.search("\.zip$",file.key)#Boolean to check if file ends with .zip
            if match: 
                zip_files.append(file)
                print("Sucess")
        if len(zip_files)!=1: #check to make sure their is no left over zips
            print("This is a failure")
            return False
        else: 
            return zip_files[0]
    # Zip Objects
    image_zip = zip_search(image_files)
    number_zip = zip_search(number_files)
    
    print("these are the number and zip files")
    print(image_zip)
    print(number_zip)
    
    # Define the payloads
    image_payload = json.dumps({"key": image_zip.key,"bucket":image_zip.bucket_name})
    number_payload = json.dumps({"key": number_zip.key,"bucket":number_zip.bucket_name})

    # Invoke the unzip lambdas function for image_zip
    unzip_lambda_client.invoke(
            FunctionName = "recognitionTrigger", 
            InvocationType = "RequestResponse",
            LogType = "None",
            Payload = image_payload
        )
    # Invoke the unzip lambdas function for image_zip

    unzip_lambda_client.invoke(
            FunctionName = "recognitionTrigger", 
            InvocationType = "RequestResponse",
            LogType = "None",
            Payload = number_payload
        )
        
        
    # We now must define the unziped directories for images and numbers 
    cow_photos =list(my_bucket.objects.filter(Prefix='image/'+ image_zip.key[:-4] + '/'))
    number_photos =list(my_bucket.objects.filter(Prefix='number/'+ number_zip.key[:-4] + '/'))
    
    
    print("This is the unzip cow and number photos directory")
    print(cow_photos)
    print(number_photos)

    # We must send each of the cow images to another 
    # lambdas function that will estimate the weight 

    # This will be what is eventually sent to the rds
    comprehensive_cow_data = []
    
    # the key attribute will allow for the access of the file path
    
    for cow_photo in cow_photos: # this is replaceing the current iteration over image files
        cow_weight = np.randomint.randomint(450,1000)#call to the api
        cow_number = i #this will be taking the slice from file.key and finding the cow number
        cow_time_stamp = i+1
        for number_photo in number_photos: 
            number_number = cow_number #number_photo.key[#]
            if cow_number == number_number: 
                number_rec_lambda = boto3.client("lambda")
                number_rec_payload = json.dumps({"key":number_photo.key})
                number_rec_lambda.invoke(
                    FunctionName = "s3_numberRec_rds", 
                    InvocationType = "RequestResponse",
                    LogType = "None",
                    Payload = number_rec_payload
                            ) 
        
        comprehensive_cow_data.append((number_number,cow_time_stamp,cow_weight,cow_number))   
        
    data = s3_client.object(BucketName=my_bucket,File_Key ="myoutput.txt")
    result = object.put(str(comprehensive_cow_data))

if __name__ == "__main__":
    # importing poisson from scipy
    from scipy.stats import poisson
 
# importing numpy as np
    import numpy as np
 
# importing matplotlib as plt
    import matplotlib.pyplot as plt
 
 
# creating a numpy array for x-axis
    x = np.arange(0, 20, 1)
 
# poisson distribution data for y-axis
    y = poisson.pmf(x, mu=5, loc=10)
 
 
# plotting the graph
    plt.plot(x, y)
 
# showing the graph
    plt.show()

        
    
    
    
    









