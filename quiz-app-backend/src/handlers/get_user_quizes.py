import json
import os
import boto3

client = boto3.client('dynamodb')

def getUserQuizes(event, context):
    print(event)
    if event["requestContext"]["http"]["method"] != "GET":
        raise Exception(f"putItemHandler only accept POST method, you tried: {event.httpMethod}")

    user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]

    data = client.query(TableName=os.environ["QUIZ_TABLE"],
                        KeyConditionExpression="PK = :pk AND begins_with(SK, :skPrefix)",
                        ExpressionAttributeValues={
                            ":pk": {"S": f"USER#{user_id}"},
                            ":skPrefix": {"S": "QUIZ#"},
                        },
                        # Optional: only return what's needed for the dropdown
                        # If any attribute name is reserved, use ExpressionAttributeNames.
                        ProjectionExpression="quiz_name, quiz_id"
                        )
    print(data)
    item = data["Items"]
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
