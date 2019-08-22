resource "aws_cloudwatch_event_rule" "every_day" {
  name = "every-day"
  description = "Fires every day"
  # 6AM UTC every day
  schedule_expression = "cron(0 6 * * ? *)"
}

resource "aws_cloudwatch_event_target" "create_badges_every_day" {
  rule = "${aws_cloudwatch_event_rule.every_day.name}"
  arn = "${aws_lambda_function.create_badges.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_create_badges" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.create_badges.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.every_day.arn}"
}
