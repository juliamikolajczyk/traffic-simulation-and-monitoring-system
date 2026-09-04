resource "docker_image" "traffic-generator" {
    name         = "${var.gcp-region}-docker.pkg.dev/${var.gcp-project}/${var.gcp-repository}/traffic-generator"
    keep_locally = false

    build {
        context  = "${path.module}/../../generator/"
        platform = "linux/amd64"
        no_cache = true
    }
}

resource "docker_registry_image" "traffic-generator" {
    name = docker_image.traffic-generator.name

    triggers = {
        image_id = docker_image.traffic-generator.repo_digest
    }
}

resource "google_cloud_run_v2_job" "traffic-generator" {
    provider              = google-beta
    name                  = "traffic-generator"
    location              = var.gcp-region
    deletion_protection   = false
    start_execution_token = "start-once-created"

    template {
        task_count  = var.generator-task-count
        parallelism = var.generator-parallelism
        template {
            timeout = "${var.exec-time + 15}s"
            containers {
                image   = docker_image.traffic-generator.name
                command = ["python", "main.py"]

                args = [
                    "-u", var.generator-user-count,
                    "-l", "http://${var.lb-ip}/logs"
                ]

                env {
                    name  = "EXEC_TIME"
                    value = var.exec-time
                }

                env {
                    name  = "URL"
                    value = var.analyzer-uri
                }

                resources {
                    limits = {
                        cpu    = var.generator-cpu
                        memory = var.generator-memory
                    }
                }
            }

            vpc_access {
                egress = "PRIVATE_RANGES_ONLY"

                network_interfaces {
                    network    = var.network-id
                    subnetwork = var.subnetwork-id
                }
            }
        }
    }

    depends_on = [docker_registry_image.traffic-generator]
}