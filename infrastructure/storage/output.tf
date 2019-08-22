output "s3_bucket_sources_id" {
  value = "${aws_s3_bucket.sources.id}"
}

output "s3_bucket_badges_id" {
  value = "${aws_s3_bucket.badges.id}"
}

output "s3_bucket_badges_arn" {
  value = "${aws_s3_bucket.badges.arn}"
}

output "s3_bucket_badges_regional_name" {
  value = "${aws_s3_bucket.badges.bucket_regional_domain_name}"
}

output "s3_bucket_logging_id" {
  value = "${aws_s3_bucket.logging.id}"
}
