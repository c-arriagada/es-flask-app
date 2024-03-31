resource "aws_api_gateway_rest_api" "estilo_calico" {
  name        = "EstiloCalico"
  description = "Estilo Calico Serverless Application"
}

# AWS API gateway
# create path
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = "${aws_api_gateway_rest_api.estilo_calico.id}"
  parent_id   = "${aws_api_gateway_rest_api.estilo_calico.root_resource_id}"
  path_part   = "{proxy+}"
}

# create http method for path above
resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = "${aws_api_gateway_rest_api.estilo_calico.id}"
  resource_id   = "${aws_api_gateway_resource.proxy.id}"
  http_method   = "ANY"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = "u4t8nh" // This cognito authorizer was created outside of terraform
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = "${aws_api_gateway_rest_api.estilo_calico.id}"
  resource_id = "${aws_api_gateway_method.proxy.resource_id}"
  http_method = "${aws_api_gateway_method.proxy.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.estilo_calico_lambda.invoke_arn}"
}

resource "aws_api_gateway_deployment" "estilo_calico" {
  depends_on = [
    aws_api_gateway_integration.lambda,
  ]

  rest_api_id = "${aws_api_gateway_rest_api.estilo_calico.id}"
#   stage_name  = "estiloCalico"
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.estilo_calico.id
  rest_api_id   = aws_api_gateway_rest_api.estilo_calico.id
  stage_name    = "prod"
}

# permission for api gateway to access lambda
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.estilo_calico_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:us-east-2:578771646113:${aws_api_gateway_rest_api.estilo_calico.id}/*/${aws_api_gateway_method.proxy.http_method}${aws_api_gateway_resource.proxy.path}"
}