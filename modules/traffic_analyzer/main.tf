resource "google_artifact_registry_repository" "repository" {
    location      = var.gcp-region
    repository_id = "repository"
    format        = "DOCKER"
}

resource "docker_image" "traffic-analyzer" {
    name         = "${var.gcp-region}-docker.pkg.dev/${var.gcp-project}/${google_artifact_registry_repository.repository.repository_id}/traffic-analyzer"
    keep_locally = false

    build {
        context  = "${path.module}/../../backend/"
        platform = "linux/amd64"
        no_cache = true
    }
}

resource "docker_registry_image" "traffic-analyzer" {
    name = docker_image.traffic-analyzer.name

    triggers = {
        image_id = docker_image.traffic-analyzer.repo_digest
    }
}

resource "google_cloud_run_v2_service" "traffic-analyzer" {
    provider            = google-beta
    name                = "traffic-analyzer"
    location            = var.gcp-region
    deletion_protection = false
    ingress             = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"
    custom_audiences    = ["http://${var.lb-ip}"]
    launch_stage        = "BETA"

    template {
        scaling {
            min_instance_count = var.analyzer-min-instance-count
            max_instance_count = var.analyzer-max-instance-count
        }

        containers {
            image = docker_image.traffic-analyzer.name

            env {
                name  = "REDIS_HOST"
                value = var.redis-host
            }

            resources {
                limits = {
                    cpu    = var.analyzer-cpu
                    memory = var.analyzer-memory
                }
                cpu_idle = false
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
    depends_on = [docker_registry_image.traffic-analyzer]
}

resource "google_cloud_run_v2_service_iam_member" "allow" {
    project  = google_cloud_run_v2_service.traffic-analyzer.project
    name     = google_cloud_run_v2_service.traffic-analyzer.name
    location = google_cloud_run_v2_service.traffic-analyzer.location
    role     = "roles/run.invoker"
    member   = "serviceAccount:${var.service-account-email}"
}