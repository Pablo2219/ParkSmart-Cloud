output "project_id" {
  value       = digitalocean_project.parksmart.id
  description = "ID del proyecto DigitalOcean."
}

output "vpc_id" {
  value       = digitalocean_vpc.parksmart.id
  description = "VPC usada por la base de datos."
}

output "registry_name" {
  value       = digitalocean_container_registry.parksmart.name
  description = "Nombre del Container Registry."
}

output "registry_endpoint" {
  value       = digitalocean_container_registry.parksmart.endpoint
  description = "Endpoint del Container Registry."
}

output "database_cluster_id" {
  value       = digitalocean_database_cluster.mysql.id
  description = "ID del clúster MySQL administrado."
}

output "database_cluster_name" {
  value       = digitalocean_database_cluster.mysql.name
  description = "Nombre del clúster MySQL para adjuntarlo a App Platform."
}

output "database_name" {
  value       = digitalocean_database_db.parksmart.name
  description = "Base de datos de ParkSmart."
}

output "database_user" {
  value       = digitalocean_database_user.parksmart.name
  description = "Usuario de aplicación creado en Managed MySQL."
}

output "database_host" {
  value       = digitalocean_database_cluster.mysql.host
  description = "Host público del clúster. No contiene credenciales."
}
