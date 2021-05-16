import os
from io import BytesIO
import boto3
import json
import base64 
import requests
from datetime import datetime

#s3 boto object
s3 = boto3.client('s3')


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
    
    if len(requestObj) == 0:
        return listKeyContents(requestObj)
    
    dir = requestObj[-1]   
    if dir == "/":
        #Notional Directory Key
        return listKeyContents(requestObj)
   
     
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
       
    else:
        
        response = generateSignedUrl(requestObj)
        
        return {
        'headers': { 'Location': response },
        'statusCode': 302
        }
    




def getObjectDirect(key):
    
    if os.environ.get('RUNMODE') == 'DEBUG':      
        print("#### SMALL OBJECT ####")
        print(key)

    response = s3.head_object(Bucket=os.environ.get('BUCKETNAME'), Key=key)
    size = response['ContentLength']
    print('###head reasponse###')
    print(response);
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
    if os.environ.get('RUNMODE') == 'DEBUG':      
        print("#### LARGE OBJECT ####")
        print(key)
  
    response = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ.get('BUCKETNAME'),'Key': key}, ExpiresIn=os.environ.get('LRG_OBJ_EXP'))
    if os.environ.get('RUNMODE') == 'DEBUG':      
        print("#### LARGE OBJECT SIGNED URL####")
        print(response)
    
    return response


def listKeyContents(key):
    
    response = s3.list_objects_v2(
    Bucket=os.environ.get('BUCKETNAME'),
    Delimiter="/",
    Prefix=key,
    EncodingType='url',
    FetchOwner=False)
    
    print("#### listKeyContents ### ")
    print(response)
    
    rtn = extractKeys(response)
    
    s = {
            'headers': { "Content-Type": "text/html" },
            'statusCode': 200,
            'body': json.dumps(rtn),
            'isBase64Encoded': False
        }
    return s
    

def extractKeys(response):
    
    rtn = []
    
    if response['KeyCount'] == 0:
        return rtn
    
    for k in response['Contents']:
        d = {}
        d['LastModified'] = k['LastModified'].strftime("%m/%d/%Y, %H:%M:%S")
        d['Key'] = k['Key']
        d['Size'] = k['Size']
        rtn.append(d)
    
    return rtn
        
    