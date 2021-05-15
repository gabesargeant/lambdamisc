import os
from io import BytesIO
import boto3
import json
import base64 

import requests

def lambda_handler(event, context):
    
    print(json.dumps(event))
    
    if os.environ.get('RUNMODE') == 'DEBUG':
        print('#### RUNMODE DEBUG -- PRINTING ENV VARIABLES')        
        print('')
        print(os.environ.get('BUCKETNAME'))
        print(os.environ.get('LRG_OBJ_EXP'))##3600 seconds
        print(os.environ.get('LRG_OBJ_LIM_BYTES'))

        print('#### RUNMODE DEBUG -- PRINTING EVENT')
        print(json.dumps(event))
        
    requestObj = event['pathParameters']['proxy']
    s3 = boto3.client('s3')
     
    if getObjectDirect(requestObj) :
        
        #requestObj = "./" + requestObj
        
        if os.environ.get('RUNMODE') == 'DEBUG':      
            print("#### SMALL OBJECT ####")
            
            print(requestObj)
        
        
        with BytesIO() as data:
            s3.download_fileobj(os.environ.get('BUCKETNAME'), requestObj, data)
            
            data.seek(0)    # move back to the beginning after writing
            return {
                'headers': { "Content-Type": "text/csv" },
                'statusCode': 200,
                'body': base64.b64encode(data.read()).decode('utf-8'),
                'isBase64Encoded': True
            }
       
        # with open(requestObj, 'wb') as f:
        #     s3.download_fileobj(os.environ.get('BUCKETNAME'), requestObj, f)
        #     return {
        #         'headers': { "Content-Type": "text/csv" },
        #         'statusCode': 200,
        #         'body': base64.b64encode(f).decode('utf-8'),
        #         'isBase64Encoded': True
        #     }
            
    else:
        generateSignedUrl("key")


    return {
        'statusCode': 200,
        'body': json.dumps('hello world')
    }


def getObjectDirect(key):
    if os.environ.get('RUNMODE') == 'DEBUG':      
        print("#### SMALL OBJECT ####")
        print(key)

    s3 = boto3.client('s3')
    response = s3.head_object(Bucket=os.environ.get('BUCKETNAME'), Key=key)
    size = response['ContentLength']
    if os.environ.get('RUNMODE') == 'DEBUG':      
        print("#### OVJECT HEAD SIZE ####")
        print("#### ", size, " ####")

    if size <= int(os.environ.get('LRG_OBJ_LIM_BYTES')):
        if os.environ.get('RUNMODE') == 'DEBUG':      
            print("#### RETURN DIRECT OBJECT AS SIZE UNDER BYTES LIM")
       
        return True
    else:
        if os.environ.get('RUNMODE') == 'DEBUG':      
            print("#### RETURN S3 SIGNED URL AS SIZE OVER BYTES LIM")
        return False ## generate a signed url.
        



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

