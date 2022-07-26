import uuid
import json, tempfile
from boto3 import client
from boto3 import resource
from boto3 import Session
from boto3.exceptions import Boto3Error #, ClientError
from botocore.exceptions import ClientError
import time
import requests

# TEMP VERSION OF THE AWS-CLIENT FOR USE UNTIL THE CDISPYUTILS ISSUE IS RESOLVED #

class BotoManager(object):
    """
    AWS manager singleton.
    """

    URL_EXPIRATION_DEFAULT = 1800  # 30 minutes
    URL_EXPIRATION_MAX = 86400  # 1 day

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        if  'aws_session_token' in config:
             self.session = Session(**config)
             self.s3_client = self.session.client('s3')
             self.sts_client = self.session.client("sts")
             self.iam = self.session.client('iam')
        else:
            self.s3_client = client('s3', **config)
            self.sts_client = client("sts", **config)
            self.iam = client('iam', **config)
        
        if 'region_name' in config:
            # self.sqs_client = client("sqs", **config)
            self.ses_client = client('ses', **config)
            self.ec2_client = client('ec2', **config)
            self.ec2_resource = resource('ec2', **config)
            self.logs_client = client('logs', **config)
        else:
            #self.sqs_client = None
            self.ses_client = None
            self.ec2_client = None
            self.ec2_resource = None
            self.logs_client = None

    def presigned_url(self, bucket, key, expires, config, method="get_object"):
        """
        Args:
            bucket (str): bucket name
            key (str): key in bucket
            expires (int): presigned URL expiration time, in seconds
            config (dict): additional parameters if necessary (e.g. updating access key)
            method (str): "get_object" or "put_object" (ClientMethod argument to boto)
        """
        if method not in ["get_object"]: #, "put_object"]:
            print("method {} not allowed".format(method))
        if "aws_access_key_id" in config:
            self.s3_client = client("s3", **config)

        expires = int(expires) or self.URL_EXPIRATION_DEFAULT
        expires = min(expires, self.URL_EXPIRATION_MAX)
        params = {"Bucket": bucket, "Key": key}
        if method == "put_object":
            params["ServerSideEncryption"] = "AES256"
        
        try:
            url_info = self.s3_client.generate_presigned_url(
                ClientMethod=method, Params=params, ExpiresIn=expires
            )
            return url_info
        except Exception as ex:
            self.logger.exception(ex)
            print(f"Failed to get pre-signed url {ex}")


    def get_object(self, bucket, key, expires, config): 
        """
        Args:
            bucket (str): bucket name
            key (str): key in bucket
            expires (int): presigned URL expiration time, in seconds
            config (dict): additional parameters if necessary (e.g. updating access key)
        """
        try:
            url = self.presigned_url(bucket, key, expires, [])
        except Exception as ex:
            self.logger.exception(ex)
            print(f"Failed to get pre-signed url for get_object: {ex}")

        try:
            retval = requests.get(url)
        except Exception as ex:
            self.logger.exception(ex)
            print(f"GET FAILED: {ex}")

        return retval.json()

    def put_json_object(self, bucket, key, expires, config, json_in): 
        """
        This function creates and uploads a file to an s3 bucket from a given json dict. 
        Args:
            bucket (str): bucket name
            key (str): key in bucket
            expires (int): presigned URL expiration time, in seconds
            config (dict): additional parameters if necessary (e.g. updating access key)
        """
        try:
            url_info = self.s3_client.generate_presigned_post(Bucket = bucket, Key = key, ExpiresIn = 30)
        except Exception as ex:
            self.logger.exception(ex)
            print(f"Failed to get pre-signed url for put_object: {ex}")

        with tempfile.NamedTemporaryFile(mode="w+") as f:
            json.dump(json_in, f)
            f.flush()
            f.seek(0)
            try:
                post_url = url_info['url']
                data = url_info['fields']
                response = requests.post(post_url, data, files={'file':f})
            except Exception as ex:
                print(f"PUT EXCEPTION: {ex}")