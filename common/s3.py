import boto3


def upload_to_s3(file_name, bucket='aap-jenkins-nightly-testresults'):
    s3 = boto3.client('s3')
    object_name = file_name
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.error(f"Failed to upload to s3 for reason: {e}")
        return False
    return True


