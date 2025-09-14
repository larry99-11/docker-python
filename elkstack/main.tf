terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Specify the AWS region
provider "aws" {
  region = "us-east-1"
}

# Generate a new private key and save it to a local file
resource "tls_private_key" "elk_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key_pem" {
  filename        = "elk-key-pair.pem"
  content         = tls_private_key.elk_key.private_key_pem
  file_permission = "400"
}

# Create a key pair in AWS using the public key
resource "aws_key_pair" "elk_key" {
  key_name   = "elk-stack-key"
  public_key = tls_private_key.elk_key.public_key_openssh
}

# Create a security group to allow inbound traffic for ELK
resource "aws_security_group" "elk_sg" {
  name_prefix = "elk-security-group"
  description = "Allow inbound traffic for the ELK stack and SSH"

  # Allow inbound HTTP traffic on port 5601 (for Kibana)
  ingress {
    from_port   = 5601
    to_port     = 5601
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow inbound Beats traffic on port 5044 (from Raspberry Pi)
  ingress {
    from_port   = 5044
    to_port     = 5044
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow inbound SSH traffic on port 22
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# Define the EC2 instance for the ELK stack
resource "aws_instance" "elk_instance" {
  # This uses an Amazon Linux 2 AMI in us-east-1 (x86_64).
  ami           = "ami-0b09ffb6d8b58ca91" 
  instance_type = "t2.medium" # Use a medium instance for more resources

  # Associate the security group
  vpc_security_group_ids = [aws_security_group.elk_sg.id]

  # Key pair for SSH access
  key_name = "elk-stack-key" 

  # User data script to install Docker and Docker Compose on launch
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo amazon-linux-extras install docker -y
              sudo systemctl start docker
              sudo usermod -aG docker ec2-user
              sudo curl -L "https://github.com/docker/compose/releases/download/v2.10.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose

              # Create directories for ELK configuration
              mkdir -p /home/ec2-user/elk-stack/logstash/pipeline
              chown -R ec2-user:ec2-user /home/ec2-user/elk-stack
              EOF

  tags = {
    Name = "ELK-Stack-Instance"
  }
}

# Output the public IP address of the EC2 instance
output "public_ip" {
  value = aws_instance.elk_instance.public_ip
}
