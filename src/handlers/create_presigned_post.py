import logging
import os
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client('s3', region_name=os.environ['AWS_REGION'], endpoint_url=('https://s3.' + os.environ['AWS_REGION'] + '.amazonaws.com'))

def create_presigned_post(event, context):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    print(event)

    bucket_name = os.environ["BUCKET_NAME"]
    user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]
    object_name = event["queryStringParameters"]["object_name"]
    quiz_id = event["queryStringParameters"]["quiz_id"]
    conditions = [
        [ "content-length-range", 1024, 1073741824 ],
        ["starts-with", "$Content-Type", "image/"],
    ]
    fields = None
    expiration=3600

    # Generate a presigned S3 POST URL
    try:
        response = s3_client.generate_presigned_post(
            bucket_name,
            user_id + '/' + quiz_id + '/' + object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        print(e)
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response