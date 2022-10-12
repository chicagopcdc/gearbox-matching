from .. import config
from . import status
from fastapi import HTTPException

def get_bucket_name():
    return config.S3_TEST_BUCKET_NAME if config.DUMMY_S3 else config.S3_BUCKET_NAME

def get_presigned_url(request, key_name, pu_config, method):
    bucket_name = get_bucket_name()
    presigned_url = ''
    try:
        presigned_url = request.app.boto_manager.presigned_url(bucket_name,key_name, config.S3_PRESIGNED_URL_EXPIRES, pu_config, method) 
    except Exception as ex:
        raise HTTPException(status.get_starlette_status(ex.code), 
            detail="Error creating presigned_url for {} {}.".format(bucket_name, ex))
    return presigned_url

def put_object(request, bucket_name, key_name, expires, config, contents):
    try:
        request.app.boto_manager.put_object(bucket_name, key_name, expires, config, contents) 
    except Exception as ex:
        raise HTTPException(status.get_starlette_status(ex.code), 
            detail="Error putting object {} {}.".format(bucket_name, ex))