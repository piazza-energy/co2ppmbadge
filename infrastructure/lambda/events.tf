resource "aws_cloudwatch_event_rule" "every_day" {
  name = "every-day"
  description = "Fires every day"
  # 6AM UTC every day
  schedule_expression = "cron(0 6 * * ? *)"
}

# runs the "every day" event on the lambda function "create_badges"
resource "aws_cloudwatch_event_target" "create_badges_every_day" {
  rule = "${aws_cloudwatch_event_rule.every_day.name}"
  arn = "${aws_lambda_function.create_badges.arn}"
}
