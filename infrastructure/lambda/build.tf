locals {
  lambda_env = "${templatefile(
    "${path.module}/templates/env_lambdas.tmpl",
    {
      region = "${var.aws_region}"
      bucket_badges = "${var.bucket_badges}"
      sns_topic_new_badges = "${var.sns_new_badges_topic_arn}"
    }
  )}"
}

resource "local_file" "env_create_badges" {
  filename = "${var.base_path_src}/serverless/create_badges/.env"
  content  = "${local.lambda_env}"
}

resource "local_file" "env_create_webview" {
  filename = "${var.base_path_src}/serverless/create_webview/.env"
  content  = "${local.lambda_env}"
}

resource "local_file" "sam_config" {
  filename = "${var.base_path_src}/config.json"
  content  = "${templatefile(
    "${path.module}/templates/sam_config.tmpl", {
      region = "${var.aws_region}"
      layer_arn = "${aws_lambda_layer_version.lambda_layer.arn}"
    }
  )}"
}

# lambda functions depending on this resource can have their .env created before they are deployed
resource "local_file" "build_version" {
  filename = "${var.base_path_src}/build.txt"
  # until we have something more clever to use
  content = "1"

  # to force a build while terraform is applying changes
  # provisioner "local-exec" {
  #   command = "make -C ${var.base_path_src} build_zips"
  # }

  # allows the .env to be created BEFORE make is run
  # lambda functions should depend on this resource to force running of make
  depends_on = [
    "local_file.env_create_badges",
    "local_file.env_create_webview"
  ]
}
