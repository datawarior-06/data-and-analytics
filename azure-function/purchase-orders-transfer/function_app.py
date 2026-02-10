import azure.functions as func
import boto3
import os
import logging
from pathlib import Path

app = func.FunctionApp()

@app.blob_trigger(
    arg_name="myblob",
    path="purchase-orders/{name}",
    connection="AzureWebJobsStorage"
)
def transfer_to_s3(myblob: func.InputStream):
    """Transfer large JSON files from Azure Blob to AWS S3"""
    
    # Extract just the filename (remove folder path)
    filename = Path(myblob.name).name
    
    logging.info(f"Processing blob: {myblob.name}, Filename: {filename}, Size: {myblob.length} bytes")
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name='eu-north-1'
    )
    
    bucket = 'purchase-orders-aws'
    key = f"source/{filename}"
    
    # Configure multipart upload for large files
    transfer_config = boto3.s3.transfer.TransferConfig(
        multipart_threshold=1024 * 25,
        max_concurrency=10,
        multipart_chunksize=1024 * 25,
        use_threads=True
    )
    
    try:
        # Upload to S3 with streaming
        s3_client.upload_fileobj(
            myblob,
            bucket,
            key,
            Config=transfer_config,
            ExtraArgs={
                'ContentType': 'application/json',
                'Metadata': {
                    'source': 'azure-blob',
                    'original-name': myblob.name
                }
            }
        )
        
        logging.info(f"✅ Successfully uploaded {filename} to s3://{bucket}/{key}")
        
    except Exception as e:
        logging.error(f"❌ Failed to upload {filename}: {str(e)}")
        raise
