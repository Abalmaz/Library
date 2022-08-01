output "ec2_public_ip" {
  value = module.mylib-server.instance.public_ip
}