import json
import boto3

dynamodb = boto3.client('dynamodb')

def get_travels():
    travels = dynamodb.scan(
            TableName='travel',
            FilterExpression = '#S = :t',
            ExpressionAttributeNames = {
                '#S':'status'
            },
            ExpressionAttributeValues = {
                ':t': {
                    "BOOL": True
                    
                }
            }
        )
    return travels

def get_last_item(travels):
    return travels[0]
    

def lambda_handler(event, context):
    travels = get_travels()
    if(travels['ResponseMetadata']['HTTPStatusCode'] == 200):
        if 'Items' in travels and travels['Count'] > 0:
            product = get_last_item(travels['Items'])
            #product = travels['Items'][0]
            id = product['travelId']['S']
            print(product)
            response = {}
            response["statusCode"] = '200'
            response['body'] = {
                'id': id
            }
            return response
        else:
            return {
                'statusCode':'404',
                'body':'No active travels'
            }
    else:
        return {
            'statusCode':travels['ResponseMetadata']['HTTPStatusCode']
        }
    
