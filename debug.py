import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Specify the local file path, S3 bucket name, and the desired path in S3
file_path = r'C:\Users\91809\Downloads\photo.jpeg'  # Use raw string to avoid unicode escape error
bucket_name = 'crmasterbucket'    # Replace with your S3 bucket name, e.g., 'my-bucket'
s3_path = 'static/photo.jpeg'  # Replace with the desired S3 path, e.g., 'uploads/myfile.txt'

# Upload the file to S3
s3.upload_file(file_path, bucket_name, s3_path)

print(f"File '{file_path}' has been uploaded to S3 bucket '{bucket_name}' at '{s3_path}'")
