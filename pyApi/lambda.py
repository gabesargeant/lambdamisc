import os
import boto3
import json

import requests

def handler(event, context):
    
    if os.environ.get('RUNMODE') == 'DEBUG':
        print('#### RUNMODE DEBUG -- PRINTING ENV VARIABLES')        
        print('')
        print(os.environ.get('BUCKETNAME'))
        print(os.environ.get('LRG_OBJ_EXP'))##3600 seconds
        print(os.environ.get(LRG_OBJ_LIM_BYTES))

        print('#### RUNMODE DEBUG -- PRINTING EVENT')
        print(event)

    getObjectDirect() 

    return {
        'statusCode': 200,
        'body': json.dumps('hello world')
    }


def getObjectDirect:
    
    s3 = boto3.client('s3')
    response = s3.head_object(Bucket='bucketname', Key='keyname')
    size = response['ContentLength']

    if size <= os.environ.get(LRG_OBJ_LIM_BYTES):
        return true
    else:
        return false ## generate a signed url.



def generateSignedUrl(key):

    client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': os.environ.get('BUCKETNAME'),
                                                            'Key': key},
                                                    ExpiresIn=os.environ.get('LRG_OBJ_EXP'))
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

