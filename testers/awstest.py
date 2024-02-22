import boto3

file = open('keys.txt', 'r')
acki = file.readline().strip()
asak = file.readline().strip()

ddb = boto3.resource(
    "dynamodb",
    region_name="ap-southeast-1",
    aws_access_key_id=acki,
    aws_secret_access_key=asak
    )

raw = ddb.Table("raw-data")

raw.put_item(Item={"timestamp": 1234})
    