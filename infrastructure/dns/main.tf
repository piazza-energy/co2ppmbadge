variable "domain_name" {}
variable "subdomain_name" {}
variable "aws_cloudfront_distribution_domain_name" {}
variable "aws_cloudfront_distribution_zone_id" {}

data "aws_route53_zone" "main" {
  name = "${var.domain_name}."
}

resource "aws_route53_record" "entrypoint" {
  zone_id = "${data.aws_route53_zone.main.zone_id}"
  name    = "${var.subdomain_name}.${var.domain_name}"
  type    = "A"

  alias {
    name                   = "${var.aws_cloudfront_distribution_domain_name}"
    zone_id                = "${var.aws_cloudfront_distribution_zone_id}"
    evaluate_target_health = false
  }
}
