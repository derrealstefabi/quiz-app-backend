import json
import os
import boto3

client = boto3.client('dynamodb')

def getAllItemsHandler(event, context):
    print(event)
    if event["requestContext"]["http"]["method"] != "GET":
        raise Exception(f"getAllItems only accept GET method, you tried: {event.httpMethod}")

    data = client.scan(TableName=os.environ["QUIZ_TABLE"])
    items = data["Items"]
    response = {
        "statusCode": 200,
        "body": json.dumps(items)
    }

    return response
