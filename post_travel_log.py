import json
import boto3

dynamodb = boto3.client('dynamodb')
get_lambda = boto3.client('lambda')

def put_item(data):
    response = dynamodb.put_item(
        TableName='travel-logs',
        Item={
            'travelId':{
                'S':data['id']
            },
            'timestamp':{
                'S':data['timestamp']
            },
            'deviceId':{
                'S':data['deviceId']
            },
            'lng':{
                'S':data['lng']
            },
            'lat':{
                'S':data['lat']
            },
            'temp':{
                'S':data['temp']
            }
        })
    print(response)

def getId():
    response = get_lambda.invoke(
        FunctionName='arn:aws:lambda:us-east-1:982253951035:function:GET_travel'
        )
    if (response['StatusCode'] != 200):
        return 0
    else:
        payload = json.load(response['Payload'])
        print(payload)
        if 'statusCode' in payload and payload['statusCode'] == '404':
            return -1
        else:
            id = payload['body']['id']
            return id

def lambda_handler(event, context):
    print(event)
    if 'Records' in event:
        record = event['Records'][0]
        data = {}
        if 'eventName' in record and record['eventName'] == 'INSERT':
            info = record['dynamodb']
            data['deviceId'] = info['Keys']['deviceId']['S']
            data['timestamp'] = info['Keys']['timestamp']['S']
            data['temp']= info['NewImage']['payload']['M']['temp']['S']
            data['lng'] = info['NewImage']['payload']['M']['lng']['S']
            data['lat'] = info['NewImage']['payload']['M']['lat']['S']
            print(data)
            data['id'] = getId()
            print(data['id'])
            if data['id'] == 0:
                return {
                    'statusCode':500,
                    'body':'Get Id'
                }
            elif data['id'] == -1:
                return {
                    'statusCode':200,
                    'body':'No active travel'
                }
            else:
                put_item(data)
        else:
            return {
                'statusCode': 200,
                'body': 'No INSERT'
            }
    else:
        return {
            'statusCode': 500,
            'body': 'We forgot to feed the hamster'
        }
