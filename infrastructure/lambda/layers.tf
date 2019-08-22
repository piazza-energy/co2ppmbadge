resource "aws_s3_bucket_object" "object_lambda_layer" {
  bucket = "${var.bucket_sources}"
  key = "lambda/layers/${var.namespace}/${var.layer_zip_name}"
  source = "${var.layer_zip_name}"

  etag = "${filemd5("${var.layer_zip_name}")}"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name = "layer_${var.namespace}"
  description = "Common layer providing all required shared libraries"

  s3_bucket = "${aws_s3_bucket_object.object_lambda_layer.bucket}"
  s3_key = "${aws_s3_bucket_object.object_lambda_layer.key}"
  s3_object_version = "${aws_s3_bucket_object.object_lambda_layer.version_id}"

  compatible_runtimes = ["python3.6"]
}
