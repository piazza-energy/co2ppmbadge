resource "aws_s3_bucket_object" "lambda_create_badges_src" {
  bucket = "${var.bucket_sources}"
  key    = "lambda/functions/${var.namespace}/${var.lambda_create_badges_zip_name}"
  source = "${var.lambda_create_badges_zip_name}"

  etag   = "${filemd5("${var.lambda_create_badges_zip_name}")}"
}

resource "aws_cloudwatch_log_group" "lambda_create_badges" {
  name              = "/aws/lambda/${var.lambda_create_badges_fn_name}"
  retention_in_days = 14
}

resource "aws_lambda_function" "create_badges" {
  s3_bucket         = "${aws_s3_bucket_object.lambda_create_badges_src.bucket}"
  s3_key            = "${aws_s3_bucket_object.lambda_create_badges_src.key}"
  s3_object_version = "${aws_s3_bucket_object.lambda_create_badges_src.version_id}"
  source_code_hash  = "${filebase64sha256("${var.lambda_create_badges_zip_name}")}"
  function_name     = "${var.lambda_create_badges_fn_name}"
  role              = "${aws_iam_role.iam_for_lambda.arn}"
  handler           = "app.lambda_handler"
  timeout           = 60
  runtime           = "python3.6"
  layers            = ["${aws_lambda_layer_version.lambda_layer.arn}"]
  depends_on        = [
    "local_file.build_version",
    "aws_iam_role_policy_attachment.lambda_logs",
    "aws_cloudwatch_log_group.lambda_create_badges"
  ]

  # environment is also set with a .env inside the distribution
  environment {
    variables = {
      S3_BUCKET = "${var.bucket_badges}"
      SNS_TOPIC_NEW_BADGES = "${var.sns_new_badges_topic_arn}"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_create_badges" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.create_badges.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.every_day.arn}"
}
