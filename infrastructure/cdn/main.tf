variable "namespace" {}
variable "stage_env" {}
variable "bucket_badges" {}
variable "bucket_badges_rn" {}
variable "bucket_logging" {}
variable "domain_name" {}

provider "aws" {
  alias = "useast1"
}

resource "aws_cloudfront_origin_access_identity" "origin_access_identity" {
  comment = "cloudfront origin access identity"
}

data "aws_acm_certificate" "cdn_cert" {
  provider = "aws.useast1"
  domain   = "${var.namespace}.${var.domain_name}"
  statuses = ["ISSUED"]
}

resource "aws_cloudfront_distribution" "s3_distribution" {

  origin {
    domain_name = "${var.bucket_badges_rn}"
    origin_id   = "${var.bucket_badges}"

    s3_origin_config {
      origin_access_identity = "${aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path}"
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "co2ppm badges"
  default_root_object = "index.html"

  logging_config {
    include_cookies = false
    bucket          = "${var.bucket_logging}.s3.amazonaws.com"
    prefix          = "co2ppm_content_logging"
  }

  aliases = ["${var.namespace}.${var.domain_name}"]

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "${var.bucket_badges}"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  # almost all edges except the most expensive ones
  # https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_DistributionConfig.html
  price_class = "PriceClass_200"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name        = "Rendered badges distribution ${var.stage_env}"
    Environment = "${var.stage_env}"
  }

  viewer_certificate {
    acm_certificate_arn      = "${data.aws_acm_certificate.cdn_cert.arn}"
    minimum_protocol_version = "TLSv1.2_2018"
    ssl_support_method       = "sni-only"
  }
}
