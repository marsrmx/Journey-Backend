import json
import boto3

dynamodb = boto3.client('dynamodb')

def parse_item(item):
    log = {}
    log['timestamp'] = item['timestamp']['S']
    log['deviceID'] = item['deviceId']['S']
    if item['temp']['S'] == 'null':
        log['temperature'] = -1
    else:
        log['temperature'] = float(item['temp']['S'])
    location = {}
    location['lat'] = item['lat']['S']
    location['long'] = item['lng']['S']
    log['location'] = location
    print(log)
    return log
    
    
def parse_items(items):
    print(items)
    travelLogs = {}
    for item in items:
        log = parse_item(item)
        travelId = item['travelId']['S']
        if travelId in travelLogs:
            travelLogs[travelId]['logs'].append(log)
        else:
            travelLogs[travelId] = {'logs': [log]}
        print(travelLogs)
    return travelLogs
        

def lambda_handler(event, context):
    res = dynamodb.scan(
        TableName='travel-logs'
        )
    print(res)
    if res['ResponseMetadata']['HTTPStatusCode'] != 200:
        return {
            'statusCode' : 500,
            'body': 'Problem reading from the database'
        }
    if res['Count'] <= 0:
        return {
            'statusCode' : 200,
            'body': 'No travels'
        }
    items = parse_items(res['Items'])
    
    return {
        'statusCode': 200,
        'TravelLogs': items
    }
