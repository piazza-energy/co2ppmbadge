variable "lambda_iam_role" {}

resource "aws_sns_topic" "new_badges" {
  name = "new-badges-created"
}

resource "aws_sns_topic_policy" "default" {
  arn    = "${aws_sns_topic.new_badges.arn}"
  policy = "${data.aws_iam_policy_document.lambda_sns_topic_handling.json}"
}

data "aws_iam_policy_document" "lambda_sns_topic_handling" {
  statement {
    actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
    ]
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["${var.lambda_iam_role}"]
    }
    resources = [
      "${aws_sns_topic.new_badges.arn}",
    ]
  }
}
