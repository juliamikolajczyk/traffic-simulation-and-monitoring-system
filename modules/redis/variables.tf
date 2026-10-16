variable "gcp-project" {
    type        = string
    description = "your project ID (e.g., my-gcp-project-123)"
}

variable "gcp-region" {
    type        = string
    description = "the GCP region (e.g., us-central1)"
}

variable "network-id" {
    type        = string
    description = "the ID of the network"
}

variable "subnetwork-id" {
    type        = string
    description = "the ID of the subnetwork"
}

variable "ip-range" {
    type        = string
    description = "the name of the allocated internal IP range reserved for VPC peering"
}

variable "redis-memory-size" {
    type        = number
    description = "the amount of RAM for Redis"
    default     = 2
}