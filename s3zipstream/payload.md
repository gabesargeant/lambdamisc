This is the payload for the Lambda. 
Use Base64 to encode it as a string. 

{  "src": "zip-test-source",
  "dst": "zip-test-dest",
  "zip":"2016 Census GCP All Geographies for AUST.zip"
}

Invoke the Lambda with: 

aws lambda invoke --function-name s3zipstream_01 --log-type Tail --payload YourBase64Encode= response.json --cli-read-timeout 600

Bump up --cli-read-timeout, which is a gloabl AWS CLI flag. If you're using the function synchronously. 

