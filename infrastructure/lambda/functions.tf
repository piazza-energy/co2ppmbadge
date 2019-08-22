resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_cloudwatch_log_group" "lambda_create_badges" {
  name              = "/aws/lambda/${var.lambda_create_badges_fn_name}"
  retention_in_days = 14
}

resource "aws_s3_bucket_object" "lambda_create_badges_src" {
  bucket = "${var.bucket_sources}"
  key    = "lambda/functions/${var.namespace}/${var.lambda_create_badges_zip_name}"
  source = "${var.lambda_create_badges_zip_name}"

  etag   = "${filemd5("${var.lambda_create_badges_zip_name}")}"
}

resource "aws_lambda_function" "create_badges" {
  s3_bucket         = "${aws_s3_bucket_object.lambda_create_badges_src.bucket}"
  s3_key            = "${aws_s3_bucket_object.lambda_create_badges_src.key}"
  s3_object_version = "${aws_s3_bucket_object.lambda_create_badges_src.version_id}"

  function_name     = "${var.lambda_create_badges_fn_name}"
  role              = "${aws_iam_role.iam_for_lambda.arn}"
  handler           = "app.lambda_handler"
  timeout           = 60

  layers            = ["${aws_lambda_layer_version.lambda_layer.arn}"]
  depends_on        = [
    "aws_iam_role_policy_attachment.lambda_logs",
    "aws_cloudwatch_log_group.lambda_create_badges"
  ]

  runtime            = "python3.6"

  environment {
    variables = {
      S3_BUCKET = "${var.bucket_badges}"
    }
  }

}
