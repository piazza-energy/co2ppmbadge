variable "namespace" {}
variable "stage_env" {}
variable "cdn_origin_access_identity_arn" {}

resource "aws_s3_bucket" "sources" {
  bucket = "${var.namespace}-sources-${var.stage_env}"
  acl    = "private"

  tags = {
    Name        = "Sources ${var.stage_env}"
    Environment = "${var.stage_env}"
  }
}

resource "aws_s3_bucket" "badges" {
  bucket = "${var.namespace}-badges-${var.stage_env}"
  acl    = "private"

  tags = {
    Name        = "Rendered badges ${var.stage_env}"
    Environment = "${var.stage_env}"
  }
}

resource "aws_s3_bucket" "logging" {
  bucket = "${var.namespace}-logging-${var.stage_env}"
  acl    = "private"

  tags = {
    Name        = "Traffic logging ${var.stage_env}"
    Environment = "${var.stage_env}"
  }
}

resource "aws_s3_bucket_policy" "badges_cdn" {
bucket = "${aws_s3_bucket.badges.id}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "CDNAccess",
  "Statement": [
    {
      "Principal": {
        "AWS": "${var.cdn_origin_access_identity_arn}"
      },
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["${aws_s3_bucket.badges.arn}"]
    },
    {
      "Sid": "OnlyCloudfrontReadAccess",
      "Principal": {
        "AWS": "${var.cdn_origin_access_identity_arn}"
      },
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": ["${aws_s3_bucket.badges.arn}/*"]
    }
  ]
}
POLICY
}

resource "aws_s3_bucket_policy" "logging_cdn" {
bucket = "${aws_s3_bucket.logging.id}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "CDNAccess",
  "Statement": [
    {
      "Principal": {
        "AWS": "${var.cdn_origin_access_identity_arn}"
      },
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["${aws_s3_bucket.logging.arn}"]
    },
    {
      "Principal": {
        "AWS": "${var.cdn_origin_access_identity_arn}"
      },
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": ["${aws_s3_bucket.logging.arn}/*"]
    }
  ]
}
POLICY
}
