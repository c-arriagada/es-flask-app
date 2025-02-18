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

locals {
    db = jsondecode(aws_secretsmanager_secret_version.estilo-calico.secret_string)
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

  runtime = "python3.8"

  layers = [aws_lambda_layer_version.deps-layer.arn]

  environment {
    variables = {
      DB_USER     = local.db.username
      DB_PASSWORD = local.db.password
      DB_HOST     = split(":",aws_db_instance.estilo_calico.endpoint)[0]
      DB_PORT     = "5432"
      DB_NAME     = aws_db_instance.estilo_calico.db_name
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
  compatible_runtimes = ["python3.8"]
}






