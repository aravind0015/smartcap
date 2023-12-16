# The code reads the input from output.txt and inserts it into DynamoDB
from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
import ssl
import datetime
import time
import struct

# Replace with your Access Key ID and Secret Access Key
aws_access_key_id = 'AKIA4V2PEK6SLYYMIQVD'
aws_secret_access_key = 'EytOaBimmD8p/4hTSFr7v4ega9hTusot5BPz4mmv'

# Specify the AWS region
aws_region = 'ap-southeast-1'

# Specify the DynamoDB table name
dynamodb_table_name = 'smartcap'

# Specify the message you want to update
message_to_update = 'MESSAGE_TO_UPDATE'

# Replace 'Your user ID here. Get it using the instruction from alexa' with your actual user ID
userId = 'AMA3QGRLPERN6GZRQJNIM3V3EOM7UNBJRO5VZJZJKCSXICFRAMKVKBHHOBU3XYOBTDAKZ67ACHTABZLCNYRRNNXSH3SC2T3Z3B4NJ3LL5KUDYS6P5AAU5BMPIN4J23JPBEFOBLGORTKLZL4Q52JJTEPCDRYOEFKZYYS476L24FCE22Z6ETDOTO5V65BDQ3USKI2LUMTI72CE7NS4NASJTMEZC34ACLET3SMPDY4AG42512SXGC5DM'

# Create an AWS session with temporary credentials
session = boto3.Session(
    aws_access_key_id='AKIA4V2PEK6SLYYMIQVD',
    aws_secret_access_key='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',
    region_name='us-east-1',
)

# Create a DynamoDB resource using the specified session
dynamodb = session.resource('dynamodb')

# Reference the table using the provided table name
table = dynamodb.Table(dynamodb_table_name)

# Helper class to convert a DynamoDB item to JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Update the item on AWS
# For that, we need guid, timestamp, and message
def call_aws(message):
    now = datetime.datetime.utcnow()
    timestamp = int(round((now - datetime.datetime(2016, 1, 1)).total_seconds()))
    timestamp_bytes = struct.pack('>q', timestamp)  # Convert timestamp to bytes

    # Your logic here...
    try:
        print("Trying to print " + message)
        response = table.update_item(
            Key={
                'guid': userId,
            },
            UpdateExpression="set tstamp= :t, command = :r",
            ExpressionAttributeValues={
                ':r': message,
                ':t': {'B': timestamp_bytes},  # Use the packed binary timestamp
            },
            ReturnValues="UPDATED_NEW"
        )
        print("UpdateItem succeeded:", response)
        return 1
    except Exception as e:
        print(e)
        with open("awserror.txt", "wb") as fol:
            fol.write(str(e))
        return e

# Main function
def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    # Open the output.txt file in read mode
    try:
        with open("output.txt", "r") as fo:
            e = call_aws(fo.read())
    except Exception as e:
        print(e)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
