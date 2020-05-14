import json
import boto3

dynamodb = boto3.client('dynamodb')

def parse_item(item):
    log = {}
    log['timestamp'] = item['timestamp']['S']
    log['deviceID'] = item['deviceId']['S']
    log['temperature'] = float(item['temp']['S'])
    location = {}
    location['lat'] = item['lat']['S']
    location['long'] = item['lng']['S']
    log['location'] = location
    print(log)
    return log

def parse_items(items):
    print(items)
    travelLog = {}
    travelLog['travelID'] = items[0]['travelId']['S']
    travelLog['logs'] = []
    for item in items:
        log = parse_item(item)
        travelLog['logs'].append(log)
    print(travelLog)
    return travelLog

def lambda_handler(event, context):
    if not 'id' in event:
        return {
            'statusCode':400,
            'body': 'Bad request'
        }
    else:
        id = event['id']
        print(id)
        res = dynamodb.query(
                TableName = 'travel-logs',
                KeyConditionExpression = 'travelId = :i',
                ExpressionAttributeValues = {
                    ':i':{
                       'S':id 
                    }
                }
            )
        print(res)
        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode' : res['ResponseMetadata']['HTTPStatusCode']
            }
        elif res['Count'] <= 0:
            return {
                'statusCode': 404,
                'body': 'The id = ' + id + ' was not found'
            }
        else:
            travelLog = parse_items(res['Items'])
            return {
                'statusCode': 200,
                'TravelLog': travelLog
            }
