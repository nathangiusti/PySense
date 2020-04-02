Module PySense.PySenseS3
========================

Functions
---------

    
`configure_versioning(bucket_name, version_config)`
:   

    
`create_bucket(bucket_name, region=None)`
:   

    
`get_bucket(bucket_name)`
:   

    
`get_buckets()`
:   

    
`upload_dashboard(bucket, dashboard, object_name)`
:   

    
`upload_file(file_name, bucket, object_name=None)`
:   Upload a file to an S3 bucket
    
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False