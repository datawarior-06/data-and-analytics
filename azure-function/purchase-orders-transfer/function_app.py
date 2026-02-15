import logging
import os
from pathlib import Path

import azure.functions as func
from azure.storage.blob import BlobServiceClient
import boto3
from botocore.exceptions import BotoCoreError, ClientError


app = func.FunctionApp()


@app.blob_trigger(
    arg_name="myblob",
    path="purchase-orders/{name}",
    connection="AzureWebJobsStorage"
)
def transfer_to_s3(myblob: func.InputStream) -> None:

    filename = Path(myblob.name).name
    blob_path = myblob.name

    logging.warning(f"Processing blob: {blob_path}")

    try:
        # Environment variables
        connection_string = os.environ["AzureWebJobsStorage"]
        bucket_name = os.environ["S3_BUCKET_NAME"]
        aws_region = os.environ["AWS_REGION"]

        # Azure Blob client
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        container_name, blob_name = blob_path.split("/", 1)

        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        logging.warning("Downloading stream from Azure...")

        downloader = blob_client.download_blob()

        # AWS S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=aws_region
        )

        s3_key = f"source/{filename}"

        logging.warning(f"Uploading to s3://{bucket_name}/{s3_key}")

        # 🚀 Reliable streaming using upload_fileobj with raw stream
        with downloader as stream:
            s3_client.upload_fileobj(
                Fileobj=stream,
                Bucket=bucket_name,
                Key=s3_key
            )

        logging.warning(f"SUCCESS: {filename} uploaded to source/")

    except (BotoCoreError, ClientError) as aws_error:
        logging.error(f"AWS ERROR: {aws_error}")
        raise

    except Exception as e:
        logging.error(f"GENERAL ERROR: {e}")
        raise
