from datetime import datetime
import uuid
from typing import List

from fastapi import HTTPException
import requests
from gearboxdatamodel.util import status
from gearboxdatamodel.util.bucket_utils import get_bucket_name
from gearbox import config
from gearbox.routers import logger

def put_object(request, bucket_name, key_name, expires, config, contents):
    try:
        request.app.boto_manager.put_object(
            bucket_name, key_name, expires, config, contents
        )
    except Exception as ex:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Error putting object {bucket_name}: {ex}.",
        )


def get_object(request, bucket_name, key_name, expires, boto_params=[], method=None):

    if config.DUMMY_S3:
        try:
            presigned_url = request.app.boto_manager.presigned_url(
                bucket_name,
                key_name,
                config.S3_PRESIGNED_URL_EXPIRES,
                boto_params,
                method,
                dummy_s3=config.DUMMY_S3,
            )
            start_idx = presigned_url.find("Signature")
            end_idx = presigned_url.find("&", start_idx)
            presigned_url = presigned_url[:start_idx] + presigned_url[end_idx + 1 :]
        except Exception as ex:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error creating presigned_url for {bucket_name} {ex}.",
            )
        try:
            response = requests.get(presigned_url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as ex:
            logger.info(
                f"HTTP Error: {ex} fetching bucket: {bucket_name} key: {key_name}"
            )
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Failed to get object: {key_name} from bucket: {bucket_name} exception: {ex}",
            )
        except Exception as ex:
            logger.exception(ex)
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Failed to get object: {key_name} from bucket: {bucket_name} exception: {ex}",
            )

    else:
        try:
            expires = 300
            response = request.app.boto_manager.get_object(
                bucket=bucket_name, key=key_name, expires=expires, config=boto_params
            )

            return response
        except Exception as ex:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error getting object {bucket_name}: {ex}.",
            )


def promote_object_to_prod(
    request,
    source_bucket: str,
    source_keys: List[str],
    dest_bucket: str,
    prod_role_arn: str
):
    """
    Copies an object from a staging S3 bucket to a production S3 bucket
    using cross-account role assumption.
    """
    try:
        sts = request.app.boto_manager.assume_role(prod_role_arn, role_session_name="staging-promote")["Credentials"]

        config = {}
        config["aws_access_key_id"] = sts["AccessKeyId"]
        config["aws_secret_access_key"] = sts["SecretAccessKey"]
        config["aws_session_token"] = sts["SessionToken"]

        deploy_id = f"{datetime.utcnow().isoformat()}-{uuid.uuid4()}"
        backup_prefix = f"_deploy_backups/{deploy_id}"
        request.app.boto_manager.assert_keys_exist(source_bucket, source_keys, config)
        
        # backup
        for key in source_keys:
            request.app.boto_manager.copy_object_between_s3(
                source_bucket=dest_bucket,
                source_key=key,
                dest_bucket=dest_bucket,
                config=config,
                dest_key=f"{backup_prefix}/{key}"
            )

        try:
            for key in source_keys:
                request.app.boto_manager.copy_object_between_s3(
                    source_bucket=source_bucket,
                    source_key=key,
                    dest_bucket=dest_bucket,
                    config=config
                )

        except Exception:
            # Rollback
            for key in source_keys:
                request.app.boto_manager.copy_object_between_s3(
                    source_bucket=dest_bucket,
                    source_key=f"{backup_prefix}/{key}",
                    dest_bucket=dest_bucket,
                    config=config,
                    dest_key=key
                )
            raise

        # Clean backups
        for key in source_keys:
            request.app.boto_manager.delete_s3_objects(
                dest_bucket, 
                f"{backup_prefix}/{key}", 
                config=config
            )

 

    except Exception as ex:
        logger.exception(f"Error promoting data to production: {ex}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Error promoting data to production from {source_bucket} to {dest_bucket} {ex}.",
        )
