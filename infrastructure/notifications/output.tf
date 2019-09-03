output "new_badges_topic_arn" {
  value = "${aws_sns_topic.new_badges.arn}"
}

output "lambda_execution_errors_topic_arn" {
  value = "${aws_sns_topic.lambda_execution_errors.arn}"
}
