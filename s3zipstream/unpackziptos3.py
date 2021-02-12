import logging
import os
from http import HTTPStatus
import boto3
import io
import traceback
import zipfile

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        
        logger.info('Event: %s', event)
        logger.info(event['src'])
        s3zipsource = event['src'] 
        dests3 = event['dst']
        
        s3_resource = boto3.resource('s3')
        zip_object = s3_resource.Object(bucket_name=event['src'], key=event['zip'])
        buffer = io.BytesIO(zip_object.get()["Body"].read())
        
        z = zipfile.ZipFile(buffer)
        for filename in z.namelist():
            file_info = z.getinfo(filename)
            s3_resource.meta.client.upload_fileobj(
                z.open(filename),
                Bucket=event['dst'],
                Key=f'{filename}'
            )

    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        raise Exception('Error occured during unpackziptoS3')
    
    return {
        "statusCode": HTTPStatus.OK.value
        
    }
