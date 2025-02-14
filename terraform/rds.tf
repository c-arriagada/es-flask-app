resource "aws_secretsmanager_secret" "estilo-calico-db" {
  name = "estilo-calico-db"
}

resource "random_password" "db_password" {
  length  = 16
  special = true
}


resource "aws_secretsmanager_secret_version" "estilo-calico" {
    secret_id     = aws_secretsmanager_secret.estilo-calico-db.id
    secret_string = jsonencode({
    username = "ec_admin",
    password = random_password.db_password.result
  })
}

locals {
    secret_data = jsondecode(aws_secretsmanager_secret_version.estilo-calico.secret_string)
}

data "aws_security_group" "existing_sg" {
  filter {
    name   = "group-name"
    values = ["subnet"]
  }
}

resource "aws_db_instance" "estilo_calico" {
  allocated_storage   = 10
  db_name             = "mydb"
  engine              = "postgres"
  engine_version      = "16.6"
  instance_class      = "db.t3.micro"
  identifier          = "estilo-calico"
  username            = local.secret_data.username
  password            = local.secret_data.password
  publicly_accessible = true
  skip_final_snapshot  = true
  
  vpc_security_group_ids = [data.aws_security_group.existing_sg.id]

#   lifecycle {
#     ignore_changes = [
#       password
#     ]
#   }
}

