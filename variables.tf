variable "gcp-project" {
    type        = string
    description = "your project ID (e.g., my-gcp-project-123)"
}

variable "gcp-region" {
    type = string
    description = "the GCP region (e.g., us-central1)"
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

variable "redis-memory-size" {
    type        = number
    description = "the amount of RAM for Redis"
    default     = 2
}