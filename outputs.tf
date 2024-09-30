# Add this output block at the end of your Terraform configuration
output "instance_public_ip" {
  value = aws_instance.web.public_ip
}
