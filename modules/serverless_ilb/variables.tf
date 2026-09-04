variable "lb-ip" {
    type        = string
    description = "load balancer's external IP address"
}

variable "cloud-run-service-name" {
    type        = string
    description = "name of the Cloud Run Service to pass the traffic to"
}

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

variable "proxy-subnetwork-id" {
    type        = string
    description = "the ID of the proxy subnetwork"
}