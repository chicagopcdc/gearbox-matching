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
            return self.s3_client.generate_presigned_url(
                ClientMethod=method, Params=params, ExpiresIn=expires
            )
        except Exception as ex:
            self.logger.exception(ex)
            print(f"EXCEPTION: {ex}")
            print("Failed to get pre-signed url")


    def get_object(self, bucket, key, expires, config): 
        """
        Args:
            bucket (str): bucket name
            key (str): key in bucket
            expires (int): presigned URL expiration time, in seconds
            config (dict): additional parameters if necessary (e.g. updating access key)
        """
        try:
            url = self.presigned_url(self, bucket, key, expires, config, method="get_object")
        except Exception as ex:
            self.logger.exception(ex)
            print("Failed to get pre-signed url for get_object")
        return requests.get(url, timeout=300)

    def put_object(self, bucket, key, expires, config, mc_json): 
        """
        Args:
            bucket (str): bucket name
            key (str): key in bucket
            expires (int): presigned URL expiration time, in seconds
            config (dict): additional parameters if necessary (e.g. updating access key)
        """
        try:
            if self.s3_client:
                print(f"YES s3 CLIENT EXISTS: {type(self.s3_client)}")
            url_info = self.s3_client.generate_presigned_post(Bucket = bucket, Key = key, ExpiresIn = 30)
            print(f"URL INFO: {url_info}")
        except Exception as ex:
            self.logger.exception(ex)
            print(f"EXCEPTION: {ex}")
            print("Failed to get pre-signed url for put_object")

        with tempfile.NamedTemporaryFile(mode="w+") as f:
            json.dump(mc_json, f)
            f.flush()
            f.seek(0)
            try:
                # print(f"PUT URL: {url_info['url']}")
                post_url = url_info['url']
                print(f"POST URL: {post_url}")
                data = url_info['fields']
                print(f"POST FIELDS: {data}")
                # response = requests.post(post_url, data, files={'file':f.name})
                response = requests.post(post_url, data, files={'file':f})
                # response = requests.post(post_url, data, files={'file': open(r'test.txt', 'rb')})
                print(f"PUT RESPONSE: {response}")
            except Exception as ex:
                print(f"PUT EXCEPTION: {ex}")