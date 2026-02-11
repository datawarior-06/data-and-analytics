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
    
    # Diagnostic logging
    logging.info(f"RAW myblob.name: '{myblob.name}'")
    logging.info(f"Path parts: {Path(myblob.name).parts}")
    
    # Extract just the filename - more explicit approach
    blob_path = Path(myblob.name)
    filename = blob_path.name
    
    logging.info(f"Extracted filename: '{filename}'")
    logging.info(f"Blob size: {myblob.length} bytes")
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name='eu-north-1'
    )
    
    bucket = 'purchase-orders-aws'
    # Use ONLY the filename, no prefix
    key = f"source/{filename}"  # Changed from f"source/{filename}"
    
    logging.info(f"Target S3 key: '{key}'")
    
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
        
        logging.info(f"✅ Successfully uploaded to s3://{bucket}/{key}")
        
    except Exception as e:
        logging.error(f"❌ Failed to upload {filename}: {str(e)}")
        raise