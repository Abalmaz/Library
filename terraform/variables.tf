variable "vpc_cidr_block" {
  default = "10.0.0.0/16"
}
variable "subnet_cidr_block" {
  default = "10.0.10.0/24"
}
variable "region" {
  default = "eu-west-3"
}
variable "avail_zone" {
  default = "eu-west-3b"
}
variable "env_pref" {
  default = "dev"
}
variable "my_ip" {
  default = "92.137.228.11/32"
}
variable "instance_type" {
  default = "t2.micro"
}
variable "image_name" {
  default = "amzn2-ami-hvm-*-x86_64-gp2"
}
variable "jenkins_ip" {
  default = "34.170.207.108/32"
}