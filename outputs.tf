output "ec2_instance_public_ip" {
  value = aws_instance.WebServer.public_ip
}
