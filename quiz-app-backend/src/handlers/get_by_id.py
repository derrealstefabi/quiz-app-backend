import json
import os
import boto3

client = boto3.client('dynamodb')

def getByIdHandler(event, context):
    if event["requestContext"]["http"]["method"] != "GET":
        raise Exception(f"getByIdHandler only accept GET method, you tried: {event.httpMethod}")

    quiz_id = event["pathParameters"]["id"]
    print(quiz_id)
    print(f"QUIZ#{quiz_id}")
    data = client.query(TableName=os.environ["QUIZ_TABLE"],
                        KeyConditionExpression="PK = :pk AND begins_with(SK, :skPrefix)",
                        ExpressionAttributeValues={
                            ":pk": {"S": f"QUIZ#{quiz_id}"},
                            ":skPrefix": {"S": "QUESTION#"},
                        })
    print(data)
    item = data["Items"]
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
