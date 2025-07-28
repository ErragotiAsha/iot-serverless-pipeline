import json
import boto3
import csv
import io
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Lambda STARTED")
    print("Event:", event)

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        print("BUCKET:", bucket_name)
        print("KEY:", key)

        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')

        try:
            json_data = json.loads(content)
            print("JSON:", json_data)
        except json.JSONDecodeError:
            print("Invalid JSON format")
            return

        if not isinstance(json_data, list):
            print("JSON root is not a list")
            return

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['sensor_id', 'zone', 'temperature', 'humidity', 'air_quality_index', 'timestamp'])

        for item in json_data:
            try:
                writer.writerow([
                    item.get('sensor_id', ''),
                    item.get('zone', ''),
                    item.get('temperature', ''),
                    item.get('humidity', ''),
                    item.get('air_quality_index', ''),
                    item.get('timestamp', '')
                ])
            except Exception as e:
                print(f"Skipping record due to error: {str(e)}")

        output_filename = f"clean/sensor_transformed_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"

        s3.put_object(
            Bucket='iot-clean-zone-bucket',
            Key=output_filename,
            Body=output.getvalue()
        )

        print(f"Uploaded cleaned CSV to: {output_filename}")
