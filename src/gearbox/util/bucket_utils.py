from gearbox import config
from gearboxdatamodel.util import status
from fastapi import HTTPException
import requests
from gearbox.routers import logger


def get_bucket_name():
    # THE S3_TEST_COMPOSE_BUCKET_NAME is used for compose testing and points to
    # a public S3 bucket containting fake mock data. The fake mock data is not used
    # for match condition or match form logic tests, so use the regular test
    # bucket for testing post requests which actually build the match and form logic and
    # post them to the back end.

    if config.DUMMY_S3:
        return config.S3_TEST_COMPOSE_BUCKET_NAME
    elif config.TESTING:
        return config.S3_TEST_BUCKET_NAME
    else:
        return config.S3_BUCKET_NAME


def get_presigned_url(request, key_name, pu_config, method):
    bucket_name = get_bucket_name()
    presigned_url = ""
    try:
        presigned_url = request.app.boto_manager.presigned_url(
            bucket_name,
            key_name,
            config.S3_PRESIGNED_URL_EXPIRES,
            pu_config,
            method,
            dummy_s3=config.DUMMY_S3,
        )

        if config.DUMMY_S3:
            start_idx = presigned_url.find("Signature")
            end_idx = presigned_url.find("&", start_idx)
            presigned_url = presigned_url[:start_idx] + presigned_url[end_idx + 1 :]
    except Exception as ex:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Error creating presigned_url for {bucket_name} {ex}.",
        )

    return presigned_url


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
