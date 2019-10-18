#!/usr/bin/env bash
pip install awscli
aws configure set aws_access_key_id $AWSKEY
aws configure set aws_secret_access_key $AWSSECRETKEY
aws configure set default.region us-east-1
aws configure set default.output json
cd custom || exit
zip -r ../lambda_function.zip -- *
cd ..
aws lambda update-function-code --function-name 'dev_buildAPlanet' --zip-file 'fileb://lambda_function.zip'