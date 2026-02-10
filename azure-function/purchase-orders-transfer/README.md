# Purchase Orders Transfer Function

Azure Function that automatically transfers files from Azure Blob Storage to AWS S3.

## Configuration

Requires these environment variables:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AzureWebJobsStorage`

## Trigger

Monitors the `purchase-orders` container in Azure Blob Storage.
