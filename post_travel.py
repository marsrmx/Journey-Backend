import json
import boto3
import uuid
import time
import math 

dynamodb = boto3.client('dynamodb')
get_lambda = boto3.client('lambda')

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

def set_travels_to_false():
    id = getId()
    print(id)
    if id == 0:
        return False
    if id == -1:
        return False
    response = get_lambda.invoke(
        FunctionName='arn:aws:lambda:us-east-1:982253951035:function:PUT_travel',
        Payload=json.dumps({'id':id})
        )
    print(response)
    return True

def parseBodyToDynamo(items):
    parsedBody = {}
    formatedItem = {}
    for itemKey in items:
        formatedItem['S'] = items[itemKey]
        parsedBody[itemKey] = formatedItem
        formatedItem = {}
    
    return parsedBody

def getItemBody(event):
    bodyItems = {}
    
    id = str(uuid.uuid1())
    bodyItems['travelId'] = id
    
    timestamp = math.trunc(time.time())
    bodyItems['timestamp'] = str(timestamp)
    
    product = "No product"
    if "product" in event:
        product = event['product']
    bodyItems['product'] = product
    
    if not 'displayName' in event:
        return 
        
    bodyItems['displayName'] = event['displayName']
    
    if 'unity' in event:
        bodyItems['unity'] = event['unity']
    
    if 'description' in event:
        bodyItems['description'] = event['description']
    
    parsedBody = {}
    parsedBody = parseBodyToDynamo(bodyItems)
    parsedBody['status'] = { 'BOOL': True }
    
    return parsedBody
    
def insert(body):
    print(body)
    try:
        response = dynamodb.put_item(
                TableName='travel',
                Item=body
            )
        print(response)
        return body['travelId']['S']
    except:
        print("ERROR -", response)
        return 0
    

def lambda_handler(event, context):
    body = getItemBody(event)
    if not body:
        return {
            'statusCode': 500
        }
        
    set_travels_to_false()
    res = insert(body)
    if(res):
        return {
            'statusCode': 200,
            'body': {'id':res }
        }
    else:
        return {
            'statusCode': 500
        }
