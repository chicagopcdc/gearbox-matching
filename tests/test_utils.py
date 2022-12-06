import re

def is_aws_url(url):
    aws_url_pattern = "^https?:\\/\\/.*s3\.amazonaws\.com"
    return True if re.match(aws_url_pattern, url) else False