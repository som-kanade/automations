import boto3
from botocore.exceptions import NoCredentialsError
import gzip

def download_and_read_logs(bucket_name, prefix, string_to_search):
    s3 = boto3.client('s3')
    total_occurrences = 0

    try:
        # List objects in the S3 bucket
        objects = s3.list_objects(Bucket=bucket_name, Prefix=prefix)

        # Iterate through each object
        for obj in objects.get('Contents', []):
            # Download the log file
            file_key = obj['Key']
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            body = response['Body'].read()

            # Check if the log file is gzipped
            if file_key.endswith('.gz'):
                body = gzip.decompress(body)

            # Decode the contents of the log file
            log_contents = body.decode('utf-8')

            # Count occurrences of the string in the log contents
            occurrences = log_contents.count(string_to_search)

            # Accumulate the total count
            total_occurrences += occurrences

            # Print the results for each log file
            print(f"Occurrences of '{string_to_search}' in {file_key}: {occurrences}")

        # Print the total count
        print(f"Total occurrences of '{string_to_search}' in all log files: {total_occurrences}")

    except NoCredentialsError:
        print("Credentials not available")

if __name__ == "__main__":
    # Replace these values with your own
    aws_access_key_id = '<aws-access-key>'
    aws_secret_access_key = '<aws-secret-key>'
    bucket_name = '<bucket-name>'
    prefix = '<path-from-logs-to-be-read>'
    string_to_search = '<string-to-search-in-s3>'

    # Set up AWS credentials
    boto3.setup_default_session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Download and read ELB logs
    download_and_read_logs(bucket_name, prefix, string_to_search)
