variable "namespace" {}
variable "bucket_sources" {}
variable "bucket_badges" {}
variable "bucket_badges_arn" {}

variable "layer_zip_name" {
  type    = "string"
  default = "layer-co2ppmbadge.zip"
}

variable "lambda_create_badges_fn_name" {
  type    = "string"
  default = "CreateBadges"
}

variable "lambda_create_badges_zip_name" {
  type    = "string"
  default = "lambda-create_badges.zip"
}
