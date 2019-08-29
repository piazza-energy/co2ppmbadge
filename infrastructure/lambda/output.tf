output "lambda_layer_arn" {
  value = "${aws_lambda_layer_version.lambda_layer.arn}"
}

output "lambda_role_arn" {
  value = "${aws_iam_role.iam_for_lambda.arn}"
}
