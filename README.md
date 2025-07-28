# IoT Serverless Data Pipeline on AWS 🚀

This repository contains all the scripts, policies, and configurations for an **end-to-end serverless IoT data pipeline** built using **AWS Lambda**, **AWS Glue**, **Amazon Athena**, **Amazon S3**, and **Amazon QuickSight**.

---

## 📌 What it does

- ✅ Raw JSON sensor data is uploaded to an **S3 raw zone bucket**.
- ✅ An **AWS Lambda function** automatically transforms raw JSON to clean CSV format.
- ✅ The **transformed CSV** is stored in a separate **S3 clean zone bucket**.
- ✅ An **AWS Glue Crawler** catalogs the cleaned CSV into an **Athena table**.
- ✅ **Athena** queries the clean data directly from S3.
- ✅ **QuickSight** visualizes live IoT metrics like temperature, humidity, and air quality.

---

## 📂 Project Structure

iot-serverless-pipeline/
├── lambda/
│ └── lambda_function.py # Lambda code: JSON → CSV transformer
├── glue/
│ └── targets.json # Glue crawler targets file
├── policies/
│ └── trust-policy.json # IAM trust policy for Lambda and Glue roles
├── queries/
│ └── sample-query.sql # Example Athena SQL queries
├── .gitignore # Ignore cache, zip, local temp files
├── README.md # This file

pgsql
Copy
Edit

---

## ⚙️ Main AWS Resources

| Resource              | Name                          | Purpose |
|-----------------------|-------------------------------|---------|
| Raw S3 Bucket         | `iot-raw-zone-bucket`         | Stores raw JSON sensor data |
| Clean S3 Bucket       | `iot-clean-zone-bucket`       | Stores transformed CSV data |
| Athena Query Results  | `iot-athena-query-results-bucket` | Athena query output |
| Lambda Function       | `JsonToCsvTransformer`        | Triggered by new JSON in raw bucket |
| Glue Crawler          | `iot_clean_crawler`           | Crawls clean CSVs to update Athena |
| Athena Database       | `iot_db`                      | Contains `clean` table |
| QuickSight Dashboard  | `IoT Dashboard`               | Visualizes the pipeline data |

---

## 🧩 How to use

1️⃣ **Upload raw JSON**  
Put a JSON file in `iot-raw-zone-bucket/raw/`:
```json
[
  {
    "sensor_id": "sensor_1234",
    "zone": "zone-1",
    "temperature": 28.5,
    "humidity": 55,
    "air_quality_index": 120,
    "timestamp": "2025-07-23T10:00:00"
  }
]
✅ Tip: It must be an array ([ ... ]) — not an object { ... }.

2️⃣ Lambda runs automatically
Lambda converts JSON → CSV → stores in iot-clean-zone-bucket/clean/.

3️⃣ Run Glue Crawler
Run iot_clean_crawler to update the clean table in Athena.

4️⃣ Query in Athena
Example:

sql
Copy
Edit
SELECT * FROM clean;
5️⃣ Visualize in QuickSight
Connect Athena → choose iot_db → table clean → build dashboards.

⚡ CLI Command Examples
bash
Copy
Edit
# Create buckets
aws s3 mb s3://iot-raw-zone-bucket
aws s3 mb s3://iot-clean-zone-bucket
aws s3 mb s3://iot-athena-query-results-bucket

# Deploy Lambda
aws lambda create-function --function-name JsonToCsvTransformer ...

# Start Glue Crawler
aws glue start-crawler --name iot_clean_crawler

# Athena query
aws athena start-query-execution \
  --query-string "SELECT * FROM clean;" \
  --query-execution-context Database=iot_db \
  --result-configuration OutputLocation=s3://iot-athena-query-results-bucket/
✅ Next Steps
✅ Automate with Step Functions.

✅ Automate infra with CloudFormation or Terraform.

✅ Schedule QuickSight to refresh for live dashboards.

📜 License
MIT — use freely, share freely!

🧑‍💻 Author
Built by [YOUR NAME] — serverless IoT pipelines made simple.

Happy Building! 
