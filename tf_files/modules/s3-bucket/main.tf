# define s3 bucket
resource "aws_s3_bucket" "gearbox_mc_bucket" {
  bucket = "${local.clean_bucket_name}"


  tags = {
    Name        = "${local.clean_bucket_name}"
    Purpose     = "Bucket to store GEARBOx match conditions"
  }
}

# turn on versioning 
resource "aws_s3_bucket_versioning" "mc_bucket_versioning" {
    bucket = aws_s3_bucket.gearbox_mc_bucket.id
    versioning_configuration {
        status = "Enabled"
    }
}

# - set noncurrent versions of match conditions file to expire in 180 days
resource "aws_s3_bucket_lifecycle_configuration" "bucket_expiration" {
    depends_on = [aws_s3_bucket_versioning.mc_bucket_versioning]
    bucket = aws_s3_bucket.gearbox_mc_bucket.bucket
    rule {
        id = "mc_bucket_expiration"
        filter {
            prefix = "match_conditions/"
        }
        noncurrent_version_expiration {
            noncurrent_days = 180
        }
        status = "Enabled"
    }
}


resource "aws_s3_bucket_acl" "gearbox_mc_bucket_acl" {
    bucket = aws_s3_bucket.gearbox_mc_bucket.id
    acl = "private"
}

resource "aws_s3_bucket" "log_bucket" {
    bucket = "${local.clean_bucket_name}-log"

  tags = {
    Name        = "${local.clean_bucket_name}-log"
    Purpose     = "GEARBOx match conditions s3 log bucket"
  }
}

resource "aws_s3_bucket_acl" "gearbox_mc_log_bucket_acl" {
    bucket = aws_s3_bucket.log_bucket.id
    acl = "log-delivery-write"
}

resource "aws_s3_bucket_logging" "bucket_logging" {
    bucket = aws_s3_bucket.gearbox_mc_bucket.id
    target_bucket = aws_s3_bucket.log_bucket.id
    target_prefix = "log/"
}

# define read only role
resource "aws_iam_role" "gearbox_mc_bucket_reader" {
  name = "bucket-reader-${local.clean_bucket_name}"
  path = "/"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

# define policy for read only role on bucket
data "aws_iam_policy_document" "gearbox_mc_bucket_reader" {
  statement {
    actions = [
      "s3:Get*",
      "s3:List*",
    ]

    effect    = "Allow"
    resources = ["${aws_s3_bucket.gearbox_mc_bucket.arn}", "${aws_s3_bucket.gearbox_mc_bucket.arn}/*"]
  }
}

# give the policy a name
resource "aws_iam_policy" "gearbox_mc_bucket_reader" {
  # This name is used in the `gen3 s3 info` function
  name        = "bucket-reader-${local.clean_bucket_name}"
  description = "Read ${local.clean_bucket_name}"
  policy      = "${data.aws_iam_policy_document.gearbox_mc_bucket_reader.json}"
}

# assign polcy to the role
resource "aws_iam_role_policy_attachment" "gearbox_mc_bucket_reader" {
  role       = "${aws_iam_role.gearbox_mc_bucket_reader.name}"
  policy_arn = "${aws_iam_policy.gearbox_mc_bucket_reader.arn}"
}

# define a container for the IAM role
resource "aws_iam_instance_profile" "gearbox_mc_bucket_reader" {
  name = "bucket-reader-${local.clean_bucket_name}"
  role = "${aws_iam_role.gearbox_mc_bucket_reader.id}"
}

#----------------------

# define bucket writer role
resource "aws_iam_role" "gearbox_mc_bucket_writer" {
  name = "bucket-writer-${local.clean_bucket_name}"
  path = "/"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

# define bucket writer policy
data "aws_iam_policy_document" "gearbox_mc_bucket_writer" {
  statement {
    actions = [
      "s3:Get*",
      "s3:List*",
    ]

    effect    = "Allow"
    resources = ["${aws_s3_bucket.gearbox_mc_bucket.arn}", "${aws_s3_bucket.gearbox_mc_bucket.arn}/*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject",
    ]

    resources = ["${aws_s3_bucket.gearbox_mc_bucket.arn}/*"]
  }
}


# define policy for read/write role on bucket
resource "aws_iam_policy" "gearbox_mc_bucket_writer" {
  # This name is used in the `gen3 s3 info` function
  name        = "bucket-writer-${local.clean_bucket_name}"
  description = "Read or write ${local.clean_bucket_name}"
  policy      = "${data.aws_iam_policy_document.gearbox_mc_bucket_writer.json}"
}

# attach policy to read/write role
resource "aws_iam_role_policy_attachment" "gearbox_mc_bucket_writer" {
  role       = "${aws_iam_role.gearbox_mc_bucket_writer.name}"
  policy_arn = "${aws_iam_policy.gearbox_mc_bucket_writer.arn}"
}

resource "aws_iam_instance_profile" "gearbox_mc_bucket_writer" {
  name = "bucket-writer-${local.clean_bucket_name}"
  role = "${aws_iam_role.gearbox_mc_bucket_writer.id}"
}
