import base64
import json
import os
import time

import boto3

client = boto3.client('dynamodb')

def randomb32():
    # Generate 10 random bytes for the identifier
    random_bytes = os.urandom(4)

    # Encode bytes to Base32, then decode to ASCII and remove padding
    identifier = base64.b32encode(random_bytes).decode('ascii').strip("=")

    return identifier


def saveQuizHandler(event, context):
    print(event)
    if event["requestContext"]["http"]["method"] != "POST":
        raise Exception(f"putItemHandler only accept POST method, you tried: {event.httpMethod}")


    now = int(time.time())
    table_name = os.environ["QUIZ_TABLE"]
    user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]
    user_name = event["requestContext"]["authorizer"]["jwt"]["claims"]["username"]
    print(user_id)

    # Get id and name from the body of the request
    body = json.loads(event["body"])
    quiz_id = randomb32()
    quiz_name = body["name"]
    name_lc = quiz_name.lower()
    questions = body["questions"]

    transact_items = [
        {
            "Put": {
                "TableName": table_name,
                "Item": {
                    "PK": {"S": f"QUIZ#{quiz_id}"},
                    "SK": {"S": "META"},
                    "owner_user_id": {"S": user_id},
                    "quiz_name": {"S": quiz_name},
                    "quiz_name_lc": {"S": name_lc},
                    "created_at": {"N": str(now)},
                },
                "ConditionExpression": "attribute_not_exists(PK)",
            }
        },
        {
            "Put": {
                "TableName": table_name,
                "Item": {
                    "PK": {"S": f"USER#{user_id}"},
                    "SK": {"S": f"QUIZ#{quiz_id}"},
                    "user_name": {"S": user_name},
                    "quiz_id": {"S": quiz_id},
                    "quiz_name": {"S": quiz_name},
                    "created_at": {"N": str(now)},
                },
                "ConditionExpression": "attribute_not_exists(PK)",
            }
        },
    ]

    for question in questions:
        print(question)
        questionId = randomb32()
        choices_list = [{"S": c} for c in (question.get("choices") or [])]

        item = {
            "PK": {"S": f"QUIZ#{quiz_id}"},
            "SK": {"S": "QUESTION#" + questionId},
            "category": {"S": question["category"]},
            "question": {"S": question["question"]},
            "answer": {"S": question["answer"]},
            "choices": {"L": choices_list},
            "points": {"S": question["points"]},
        }

        image = question.get("image")
        if image:
            item["image"] = {"S": image}

        transact_items.append({
            "Put": {
                "TableName": table_name,
                "Item": item,
            }
        })

    result = client.transact_write_items(
        TransactItems=transact_items
    )

    response = {
        "statusCode": 200,
        "body": json.dumps({
            'quiz_id': quiz_id
        })
    }

    return response
