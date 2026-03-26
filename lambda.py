import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    print("Checking S3 buckets for encryption...\n")
    
    buckets = s3.list_buckets()['Buckets']
    
    unencrypted_buckets = []
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        
        try:
            response = s3.get_bucket_encryption(Bucket=bucket_name)
            print(f"[ENCRYPTED] {bucket_name}")
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                print(f"[NOT ENCRYPTED] {bucket_name}")
                unencrypted_buckets.append(bucket_name)
            else:
                print(f"[ERROR] {bucket_name} - {e}")
    
    print("\nSummary:")
    print(f"Unencrypted Buckets: {unencrypted_buckets}")
    
    return {
        "statusCode": 200,
        "unencrypted_buckets": unencrypted_buckets
    }
