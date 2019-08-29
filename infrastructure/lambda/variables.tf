variable "namespace" {}
variable "aws_region" {}
variable "bucket_sources" {}
variable "bucket_badges" {}
variable "bucket_badges_arn" {}
variable "sns_new_badges_topic_arn" {}
variable "base_path_src" {}

variable "layer_zip_name" {
  type    = "string"
  default = "layer-co2ppmbadge.zip"
}

variable "lambda_create_badges_fn_name" {
  type    = "string"
  default = "CO2PPM-CreateBadges"
}

variable "lambda_create_webview_fn_name" {
  type    = "string"
  default = "CO2PPM-CreateWebview"
}

variable "lambda_create_badges_zip_name" {
  type    = "string"
  default = "lambda-create_badges.zip"
}

variable "lambda_create_webview_zip_name" {
  type    = "string"
  default = "lambda-create_webview.zip"
}
