# quiz-app-backend
[![.github/workflows/deploy.yml](https://github.com/derrealstefabi/quiz-app-backend/actions/workflows/deploy.yml/badge.svg)](https://github.com/derrealstefabi/quiz-app-backend/actions/workflows/deploy.yml)

Backend for the [quiz-app](https://github.com/derrealstefabi/quiz-app) repository.
Contains the AWS infrastructure needed to save and load quizzes.

A push to the main branch of this repo triggers an automatic deployment of the changes to AWS, as well as a deployment of the quiz-app frontend.

## Contains:
* DynamoDB table to save quizzes
* HttpApi Endpoints:
  * get_user_quizzes (GET /quiz)
    * fetch metadata for all of a user's quizzes
  * get_by_id (GET /quiz/{id})
    * get all data for a specific quiz (name, user, questions)
  * save_quiz (POST /quiz)
    * save a quiz to DynamoDB
  * create_presigned_post (GET /createPresignedPost)
    * create a presigned POST link for image upload to s3
  * create_presigned_get (POSWGETT /createPresignedGet)
      * create a presigned url (GET) link for image retrieval from s3
* Cognito Userpool for Authentication


## Prerequisites:
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).


## Build and deploy to AWS
To deploy the backend to CloudFormation, run the following:
```bash
sam build
sam deploy --guided
```

## Cleanup
To delete the stack from CloudFormation, run the following:

```bash
sam delete --stack-name "quiz-app-backend"
```
