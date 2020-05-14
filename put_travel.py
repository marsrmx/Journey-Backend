import json
import boto3
import time
import math

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    if not 'id' in event:
        return {
            'statusCode':400,
            'body': 'Bad Request'
        }
    travelId = event['id']
    timestamp = math.trunc(time.time())
    response = dynamodb.update_item(
        TableName = 'travel',
        Key = {
            'travelId':{
                'S':travelId
            }
        },
        UpdateExpression = 'SET #S = :f, #E = :e',
        ExpressionAttributeNames = {
            "#S":'status',
            "#E":'endtimestamp'
        },
        ExpressionAttributeValues = {
            ':f':{
                'BOOL':False
            },
            ':e':{
                'S':str(timestamp)
            }
        })
    if(response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'statusCode': 200,
            'body': 'Status of '+ travelId +' change to false'
        }
    else:
        return {
            'statusCode':response['ResponseMetadata']['HTTPStatusCode']
        }
