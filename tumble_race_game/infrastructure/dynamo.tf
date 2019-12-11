
resource "aws_dynamodb_table" "connections" {
  name           = "connections"
  hash_key       = "connection_id"
  billing_mode = "PAY_PER_REQUEST"
  stream_enabled = "true"
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "connection_id"
    type = "S"
  }


  ttl {
    attribute_name = "ttl",
    enabled = true
  }

  tags {
    Name        = "connections"
    Environment = "${data.terraform_remote_state.config.run_env}"
    owner = "devops"
    application = "devops.ci"
  }
}

resource "aws_dynamodb_table" "_auth" {
  name           = "auth"
  hash_key       = "token_id"
  billing_mode = "PAY_PER_REQUEST"
  attribute {
    name = "token_id"
    type = "S"
  }

  ttl {
    attribute_name = "ttl",
    enabled = true
  }

  tags {
    Name        = "auth"
    Environment = "${data.terraform_remote_state.config.run_env}"
    owner = "devops"
    application = "devops.ci"
  }
}
