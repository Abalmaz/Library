terraform {
  backend "s3" {
    bucket = "mylib-bucket"
    key    = "library/state.tfstate"
    region = "eu-west-3"
  }
}

provider "aws" {
  region = var.region
}

resource "aws_vpc" "mylib-vpc" {
  cidr_block = var.vpc_cidr_block
  tags       = {
    Name : "${var.env_pref}-vpc"
  }
}

module "mylib-subnet" {
  source                 = "modules/subnet"
  avail_zone             = var.avail_zone
  default_route_table_id = aws_vpc.mylib-vpc.default_route_table_id
  env_pref               = var.env_pref
  subnet_cidr_block      = var.subnet_cidr_block
  vpc_id                 = aws_vpc.mylib-vpc.id
}

module "mylib-server" {
  source        = "modules/webserver"
  avail_zone    = var.avail_zone
  env_pref      = var.env_pref
  image_name    = var.image_name
  instance_type = var.instance_type
  my_ip         = var.my_ip
  jenkins_ip    = var.jenkins_ip
  subnet_id     = module.mylib-subnet.subnet.id
  vpc_id        = aws_vpc.mylib-vpc.id
}