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

data "archive_file" "estilo_calico_flask_app" {
  type        = "zip"
  output_path = "estilo_calico_backend.zip"
  source {
    content = file("${path.module}/../app.py")
    filename = "app.py"
  }
  source {
    content = file("${path.module}/../db.py")
    filename = "db.py"
  }
  source {
    content = file("${path.module}/../events.py")
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

  source_code_hash = "${filebase64sha256("./estilo_calico_backend.zip")}"
  depends_on = [data.archive_file.estilo_calico_flask_app ]

  runtime = "python3.11"

  layers = [aws_lambda_layer_version.deps-layer.arn]
#   environment {
#     variables = {
#       foo = "bar"
#     }
#   }
}

resource "aws_lambda_layer_version" "deps-layer" {
    filename            = "../estilo-calico-deps-layer.zip"
    layer_name          = "estilo-calico-deps"
    source_code_hash    = "${filebase64sha256("../estilo-calico-deps-layer.zip")}"
    compatible_runtimes = ["python3.11"]
}