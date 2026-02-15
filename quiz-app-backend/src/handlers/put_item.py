import json
import os
import boto3

client = boto3.client('dynamodb')

def putItemHandler(event, context):
    print(event)
    if event["requestContext"]["http"]["method"] != "POST":
        raise Exception(f"putItemHandler only accept POST method, you tried: {event.httpMethod}")

    # Get id and name from the body of the request
    body = json.loads(event["body"])
    sk = body["SK"]
    pk = body["PK"]
    question = body["question"]
    answer = body["answer"]
    image = body["image"]
    choices = body["choices"]
    points = body["points"]

    result = client.put_item(TableName=os.environ["QUIZ_TABLE"], Item={
        "PK": {"S": pk},
        "SK": {"S": sk},
        "question": {"S": question or ""},
        "answer": {"S": answer or ""},
        "image": {"S": image or ""},
        "choices": {"S": choices or ""},
        "points": {"S": points or ""}
    })
    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response
