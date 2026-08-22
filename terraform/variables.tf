variable "project_name" {
  type        = string
  default     = "parksmart"
  description = "Nombre base del proyecto."
}

variable "environment" {
  type        = string
  default     = "prod"
  description = "Entorno de despliegue."
}

variable "region" {
  type        = string
  default     = "nyc3"
  description = "Región de DigitalOcean para la base de datos y VPC."
}

variable "vpc_ip_range" {
  type        = string
  default     = "10.20.0.0/24"
  description = "Rango privado de la VPC de ParkSmart."
}

variable "database_size" {
  type        = string
  default     = "db-s-1vcpu-1gb"
  description = "Plan del nodo MySQL administrado."
}

variable "database_node_count" {
  type        = number
  default     = 1
  description = "Cantidad de nodos. Usar 2 si el presupuesto permite alta disponibilidad con standby."

  validation {
    condition     = var.database_node_count >= 1 && var.database_node_count <= 3
    error_message = "database_node_count debe estar entre 1 y 3."
  }
}

variable "database_name" {
  type        = string
  default     = "parksmart"
  description = "Base de datos de la aplicación."
}

variable "database_user" {
  type        = string
  default     = "parksmart_app"
  description = "Usuario normal usado por la aplicación y las migraciones del proyecto académico."
}

variable "registry_name" {
  type        = string
  default     = "cr-parksmart-prod"
  description = "Nombre global del DigitalOcean Container Registry. Debe ser único en la cuenta."
}
