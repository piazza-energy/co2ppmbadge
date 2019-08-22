variable "aws_profile" {}
variable "aws_region" {}
variable "namespace" {}
variable "domain_name" {}
variable "stage_env" {}

provider "aws" {
  region                  = "${var.aws_region}"
  shared_credentials_file = "~/.aws/credentials"
  profile                 = "${var.aws_profile}"
  version                 = "~> 2.0"
}

provider "aws" {
  alias                   = "useast1"
  region                  = "us-east-1"
  shared_credentials_file = "~/.aws/credentials"
  profile                 = "${var.aws_profile}"
  version                 = "~> 2.0"
}

provider "local" {
  version = "~> 1.3"
}

module "storage" {
  source                         = "./storage"
  namespace                      = "${var.namespace}"
  stage_env                      = "${var.stage_env}"
  cdn_origin_access_identity_arn = "${module.cdn.cdn_origin_access_identity_arn}"
}

module "lambda" {
  source            = "./lambda"
  namespace         = "${var.namespace}"
  bucket_sources    = "${module.storage.s3_bucket_sources_id}"
  bucket_badges     = "${module.storage.s3_bucket_badges_id}"
  bucket_badges_arn = "${module.storage.s3_bucket_badges_arn}"
}

module "dns" {
  source                                  = "./dns"
  domain_name                             = "${var.domain_name}"
  subdomain_name                          = "${var.namespace}"
  aws_cloudfront_distribution_zone_id     = "${module.cdn.aws_cloudfront_distribution_zone_id}"
  aws_cloudfront_distribution_domain_name = "${module.cdn.aws_cloudfront_distribution_domain_name}"
}

module "cdn" {
  source           = "./cdn"
  providers        = {
    aws = "aws"
    aws.useast1 = "aws.useast1"
  }
  namespace        = "${var.namespace}"
  stage_env        = "${var.stage_env}"
  bucket_badges    = "${module.storage.s3_bucket_badges_id}"
  bucket_badges_rn = "${module.storage.s3_bucket_badges_regional_name}"
  bucket_logging   = "${module.storage.s3_bucket_logging_id}"
  domain_name      = "${var.domain_name}"
}

resource "local_file" "env_create_badges" {
  filename = "${path.cwd}/../co2ppmbadge/serverless/create_badges/.env"
  content  = templatefile(
    "${path.cwd}/templates/env_create_badges.tmpl", {
      region = "${var.aws_region}"
      bucket_badges = "${module.storage.s3_bucket_badges_id}"
    }
  )
}

resource "local_file" "sam_config" {
  filename = "${path.cwd}/../co2ppmbadge/config.json"
  content  = templatefile(
    "${path.cwd}/templates/sam_config.tmpl", {
      region = "${var.aws_region}"
      layer_arn = "${module.lambda.lambda_layer_arn}"
    }
  )
}
