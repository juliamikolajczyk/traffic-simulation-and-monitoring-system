variable "gcp-project" {
    type        = string
    description = "your project ID (e.g., my-gcp-project-123)"
}

variable "gcp-region" {
    type = string
    description = "the GCP region (e.g., us-central1)"
}

variable "network-id" {
    type = string
    description = "the ID of the network"
}

variable "subnetwork-id" {
    type = string
    description = "the ID of the subnetwork"
}

variable "redis-host" {
    type        = string
    description = "the IP address of Redis"
}

variable "service-account-email" {
    type = string
    description = "the email address of the service account"
}

variable "generator-task-count" {
    type = number
    description = "the total number of generator instances that need to be run to complete the job"
    default = 5
}

variable "generator-parallelism" {
    type = number
    description = "the maximum number of tasks that can be run at the exact same time"
    default = 10
}

variable "generator-user-count" {
    type = string
    description = "the number of users generating traffic from an instance"
    default = "5"
}

variable "generator-cpu" {
    type = string
    description = "the number of CPU cores allocated to each generator instance"
    default = "2"
}

variable "generator-memory" {
    type = string
    description = "the amount of RAM allocated to each generator instance"
    default = "2Gi"
}

variable "analyzer-cpu" {
    type = string
    description = "the number of CPU cores allocated to each analyzer instance"
    default = "2"
}

variable "analyzer-memory" {
    type = string
    description = "the amount of RAM allocated to each analyzer instance"
    default = "2Gi"
}

variable "analyzer-min-instance-count" {
    type = number
    description = "the minimum number of analyzer instances"
    default = 1
}

variable "analyzer-max-instance-count" {
    type = number
    description = "the maximum number of analyzer instances"
    default = 10
}

variable "exec-time" {
    type = number
    description = "for how many seconds the traffic is generated (e.g., 3400); must be less than or equal to 604715"
    default = 600
}