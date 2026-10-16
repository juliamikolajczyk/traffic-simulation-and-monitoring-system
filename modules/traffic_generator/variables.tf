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

variable "generator-task-count" {
    type        = number
    description = "the total number of generator instances that need to be run to complete the job"
    default     = 5
}

variable "generator-parallelism" {
    type        = number
    description = "the maximum number of tasks that can be run at the exact same time"
    default     = 10
}

variable "generator-user-count" {
    type        = string
    description = "the number of users generating traffic from an instance"
    default     = "5"
}

variable "generator-cpu" {
    type        = string
    description = "the number of CPU cores allocated to each generator instance"
    default     = "2"
}

variable "generator-memory" {
    type        = string
    description = "the amount of RAM allocated to each generator instance"
    default     = "2Gi"
}

variable "exec-time" {
    type        = number
    description = "for how many seconds the traffic is generated (e.g., 3400); must be less than or equal to 604715"
    default     = 600
}

variable "lb-ip" {
    type        = string
    description = "load balancer's external IP address"
}

variable "gcp-repository" {
    type        = string
    description = "the ID of the registry repository"
}

variable "analyzer-uri" {
    type        = string
    description = "traffic analyzer's URI"
}