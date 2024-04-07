data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "lambda_s3_access" {
  name        = "lambda_s3_access_policy"
  description = "IAM policy for allowing Lambda to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::estilocalico-bucket*",
        ]
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_access_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_s3_access.arn
}


data "archive_file" "estilo_calico_flask_app" {
  type        = "zip"
  output_path = "estilo_calico_backend.zip"
  source {
    content  = file("${path.module}/../app.py")
    filename = "app.py"
  }
  source {
    content  = file("${path.module}/../db.py")
    filename = "db.py"
  }
  source {
    content  = file("${path.module}/../events.py")
    filename = "events.py"
  }
}

resource "aws_lambda_function" "estilo_calico_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "./estilo_calico_backend.zip"
  function_name = "estilo_calico_backend"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "app.lambda_handler"
  timeout       = 15
  memory_size   = 2048

  source_code_hash = filebase64sha256("./estilo_calico_backend.zip")
  depends_on       = [data.archive_file.estilo_calico_flask_app]

  runtime = "python3.9"

  layers = [aws_lambda_layer_version.deps-layer.arn]

  environment {
    variables = {
      DB_URI      = "postgres://dygltzkk:xqtNJSqVix9ds-0kv97UYDo-5Iif9CsH@hansken.db.elephantsql.com/dygltzkk"
      DB_USER     = jsondecode(data.aws_secretsmanager_secret_version.secret-version.secret_string)["DB_USER"]
      DB_PASSWORD = jsondecode(data.aws_secretsmanager_secret_version.secret-version.secret_string)["DB_PASSWORD"]
      DB_HOST     = "hansken.db.elephantsql.com"
      DB_PORT     = "5432"
    }
  }
  lifecycle {
    ignore_changes = [source_code_hash]
  }
}

resource "aws_lambda_layer_version" "deps-layer" {
  filename            = "../estilo-calico-deps-layer.zip"
  layer_name          = "estilo-calico-deps"
  source_code_hash    = filebase64sha256("../estilo-calico-deps-layer.zip")
  compatible_runtimes = ["python3.9"]
}

resource "aws_secretsmanager_secret" "estilo_calico_admin" {
  name = "estilo_calico_admin"
}

data "aws_secretsmanager_secret_version" "secret-version" {
  secret_id = aws_secretsmanager_secret.estilo_calico_admin.id
}




