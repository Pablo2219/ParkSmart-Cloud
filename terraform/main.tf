resource "digitalocean_project" "parksmart" {
  name        = "${var.project_name}-${var.environment}"
  description = "Infraestructura cloud de ParkSmart"
  purpose     = "Web Application"
  environment = "Production"
}

resource "digitalocean_vpc" "parksmart" {
  name     = "vpc-${var.project_name}-${var.environment}"
  region   = var.region
  ip_range = var.vpc_ip_range
}

resource "digitalocean_container_registry" "parksmart" {
  name                   = var.registry_name
  subscription_tier_slug = "basic"
}

resource "digitalocean_database_cluster" "mysql" {
  name                 = "mysql-${var.project_name}-${var.environment}"
  engine               = "mysql"
  version              = "8.4"
  size                 = var.database_size
  region               = var.region
  node_count           = var.database_node_count
  private_network_uuid = digitalocean_vpc.parksmart.id
  tags                 = [var.project_name, var.environment]
}

resource "digitalocean_database_db" "parksmart" {
  cluster_id = digitalocean_database_cluster.mysql.id
  name       = var.database_name
}

resource "digitalocean_database_user" "parksmart" {
  cluster_id        = digitalocean_database_cluster.mysql.id
  name              = var.database_user
  mysql_auth_plugin = "caching_sha2_password"
}

resource "digitalocean_database_mysql_config" "parksmart" {
  cluster_id        = digitalocean_database_cluster.mysql.id
  default_time_zone = "+00:00"
  slow_query_log    = true
  long_query_time   = 2
}

resource "digitalocean_project_resources" "database" {
  project = digitalocean_project.parksmart.id
  resources = [
    digitalocean_database_cluster.mysql.urn,
  ]
}
