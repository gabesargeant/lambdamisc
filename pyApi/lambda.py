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
    print("REQUEST OBJCT : ", requestObj)
    
    if len(requestObj) == 0:
        requestObj = "/"
    
    if requestObj[-1] == "/":
        return listKeyContents(requestObj)
        
    response = s3.head_object(Bucket=os.environ.get('BUCKETNAME'), Key=requestObj)
    print('### head reasponse ###')
    print(response);
    size = response['ContentLength']
    content_type = response['ContentType']
    
    if os.environ.get('RUNMODE') == 'DEBUG':      
        print("#### OVJECT HEAD SIZE ####")
        print("#### ", size, " ####")
    
    
    if  size <= int(os.environ.get('LRG_OBJ_LIM_BYTES')) :
        
        if os.environ.get('RUNMODE') == 'DEBUG':      
            print("#### RETURN DIRECT OBJECT AS SIZE UNDER BYTES LIM")
            print(requestObj)
        
        with BytesIO() as data:
            s3.download_fileobj(os.environ.get('BUCKETNAME'), requestObj, data)
            
            data.seek(0)    # move back to the beginning after writing
            return {
                'headers': { "Content-Type": content_type },
                'statusCode': 200,
                'body': base64.b64encode(data.read()).decode('utf-8'),
                'isBase64Encoded': True
            }
       
    else:
        if os.environ.get('RUNMODE') == 'DEBUG':      
            print("#### RETURN S3 SIGNED URL AS SIZE OVER BYTES LIM")
        response = generateSignedUrl(requestObj)
        
        return {
        'headers': { 'Location': response },
        'statusCode': 302
        }


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
    
    prefix = key
    
    
    if key == "/":
        prefix = ""
        
    
    print("prefix ", prefix)
    
    
    response = s3.list_objects_v2(
    Bucket=os.environ.get('BUCKETNAME'),
    Delimiter="/",
    Prefix=prefix,
    EncodingType='url',
    FetchOwner=False)
    
    print("#### listKeyContents ### ")
    print(response)
    
    
    print("#### COMMON PREFIXES ### ")
    prefixes = []
    if "CommonPrefixes" in response:
        prefixes = response['CommonPrefixes']


    rtn = extractKeys(response, prefixes)
    rootpath = os.environ.get("ROOTPATH")     
    
    templateTop = """
        <html>
        <head>
        <title>"""
        
    templateTop+=rootpath+key
    
    templateHead = """</title>
        </head>
        <body>
        <table>
        <tr><th>LastModified</th><th>Size</th><th>Key</th></tr>
    """
    templateTop+=templateHead
    
    templateTail = """
        </table>
        </body>
        <html>
    """
   
    
    for x in rtn:
        templateTop += "<tr><td>" + x['LastModified'] + "</td><td>" + str(x['Size']) + "</td><td><a href=\"" + x['Key'] + "\">" + x['Key'] + "</a></td></tr>"
    
    templateTop += templateTail
    
    
    s = {
            'headers': { "Content-Type": "text/html" },
            'statusCode': 200,
            'body': templateTop
        }
    return s
    

def extractKeys(response, prefixes):
    rootpath = os.environ.get("ROOTPATH")     
    rtn = []

    for p in prefixes:
        d = {}
        d['LastModified'] = "---"
        d['Key'] = rootpath+p['Prefix']
        d['Size'] = "dir"
        rtn.append(d)

    if response['KeyCount'] == 0:
        return rtn
    
    for k in response['Contents']:
        d = {}
        d['LastModified'] = k['LastModified'].strftime("%m/%d/%Y, %H:%M:%S")
        d['Key'] = rootpath+k['Key']
        d['Size'] = k['Size']
        rtn.append(d)
    
    return rtn
        

