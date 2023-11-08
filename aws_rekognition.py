import boto3
import signal
import sys
import json

# To handle the SIGINT when CTRL+C is pressed
def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    sys.exit(1)

# AWS access and secret key
aws_access_key_id = 'AKIA4V2PEK6SLYYMIQVD'
aws_secret_access_key = 'EytOaBimmD8p/4hTSFr7v4ega9hTusot5BPz4mmv'
aws_region = 'ap-southeast-1' # Change to your desired AWS region

# Initialize the Amazon Rekognition client
rekognition = boto3.client('rekognition', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Saves the text to the file
def saveTextFile(text):
    try:
        print(text)
        with open("output.txt", "w+") as text_file:
            text_file.write(text)
    except Exception as e:
        print("Exception occurred")
        print(e)

def read_image():
    path_to_file_in_disk = 'smart_cap.png'
    with open(path_to_file_in_disk, 'rb') as f:
        data = f.read()
    return data

def analyze_image(data):
    try:
        response = rekognition.detect_labels(
            Image={
                'Bytes': data
            }
        )
        print(json.dumps(response, indent=2))
        return response
    except Exception as e:
        print("An error occurred:", e)
        return None

def tag_from_data(input):
    if input is not None and 'Labels' in input:
        # Get image labels
        labels = input['Labels']
        label_names = [label['Name'] for label in labels]

        # Construct the result string
        awsstring = "Amazon Rekognition detected the following labels: "
        awsstring += ', '.join(label_names)

        return awsstring

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    img = read_image()
    data = analyze_image(img)
    text = tag_from_data(data)
    saveTextFile(text)
