# main.tf
provider "aws" {
  region = "ap-south-1" # Set your desired region
}

# Data block to reference the existing subnet
data "aws_subnet" "my_subnet" {
  id = "subnet-0a69df4cd6adac61f"  # Your existing subnet ID
}

# Create a VPC (if necessary; otherwise, use your existing VPC)
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "my_vpc"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id

  tags = {
    Name = "my_igw"
  }
}

# Create a Route Table
resource "aws_route_table" "my_route_table" {
  vpc_id = aws_vpc.my_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_igw.id
  }

  tags = {
    Name = "my_route_table"
  }
}

# Associate Route Table with the Existing Subnet
resource "aws_route_table_association" "my_route_table_association" {
  subnet_id      = data.aws_subnet.my_subnet.id
  route_table_id = aws_route_table.my_route_table.id
}

# Create an EC2 Instance using the existing subnet
resource "aws_instance" "my_instance" {
  ami                    = "ami-08718895af4dfa033" # Your specified AMI ID
  instance_type         = "t2.micro"
  subnet_id             = data.aws_subnet.my_subnet.id  # Reference the existing subnet
  key_name              = "hello"                        # Your specified key pair name
  vpc_security_group_ids = ["sg-06407c75608a7a5e9"]     # Your specified security group ID

  tags = {
    Name = "my_instance"
  }
}

# Create an API Gateway
resource "aws_api_gateway_rest_api" "my_api" {
  name        = "my_api"
  description = "My API"
}

# Create a Resource in the API Gateway
resource "aws_api_gateway_resource" "my_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "myresource"
}

# Create a Method for the Resource
resource "aws_api_gateway_method" "my_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.my_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

