



resource "aws_s3_bucket_object" "lambda_create_webview_src" {
  bucket = "${var.bucket_sources}"
  key    = "lambda/functions/${var.namespace}/${var.lambda_create_webview_zip_name}"
  source = "${var.lambda_create_webview_zip_name}"

  etag   = "${filemd5("${var.lambda_create_webview_zip_name}")}"
}

resource "aws_cloudwatch_log_group" "lambda_create_webview" {
  name              = "/aws/lambda/${var.lambda_create_webview_fn_name}"
  retention_in_days = 14
}

resource "aws_lambda_function" "create_webview" {
  s3_bucket         = "${aws_s3_bucket_object.lambda_create_webview_src.bucket}"
  s3_key            = "${aws_s3_bucket_object.lambda_create_webview_src.key}"
  s3_object_version = "${aws_s3_bucket_object.lambda_create_webview_src.version_id}"
  source_code_hash  = "${filebase64sha256("${var.lambda_create_webview_zip_name}")}"
  function_name     = "${var.lambda_create_webview_fn_name}"
  role              = "${aws_iam_role.iam_for_lambda.arn}"
  handler           = "app.lambda_handler"
  timeout           = 60
  runtime           = "python3.6"
  layers            = ["${aws_lambda_layer_version.lambda_layer.arn}"]
  depends_on        = [
    "local_file.build_version",
    "aws_iam_role_policy_attachment.lambda_logs",
    "aws_cloudwatch_log_group.lambda_create_webview"
  ]

  # environment is also set with a .env inside the distribution
  environment {
    variables = {
      S3_BUCKET = "${var.bucket_badges}"
    }
  }
}

resource "aws_lambda_permission" "allow_sns_to_call_create_webview" {
    statement_id = "AllowExecutionFromSNS"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.create_webview.function_name}"
    principal = "sns.amazonaws.com"
    source_arn = "${var.sns_new_badges_topic_arn}"
}

resource "aws_sns_topic_subscription" "lambda_create_webview" {
  topic_arn = "${var.sns_new_badges_topic_arn}"
  protocol  = "lambda"
  endpoint  = "${aws_lambda_function.create_webview.arn}"
}
