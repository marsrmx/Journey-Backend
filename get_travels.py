import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    response = dynamodb.scan(
        TableName='travel'
        )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200 and response['Items'] > 0:
        return { 'statusCode':response['ResponseMetadata']['HTTPStatusCode'] }
    
    items = response['Items']
    travels = []
    travel = {}
    for item in items:
        travel['travelId'] = item['travelId']['S']
        travel['product'] = item['product']['S']
        travel['status'] = item['status']['BOOL']
        travel['timestamp'] = item['timestamp']['S']
        travel['displayName'] = item['displayName']['S']
        if 'endtimestamp' in item:
            travel['endtimestamp'] = item['endtimestamp']['S']
        if 'description' in item:
            travel['description'] = item['description']['S']
        travel['unity'] = item['unity']['S']
        travels.append(travel)
        travel = {}
    return travels
