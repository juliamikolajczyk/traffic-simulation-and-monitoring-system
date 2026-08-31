resource "google_artifact_registry_repository" "repository" {
    location      = var.gcp-region
    repository_id = "repository"
    format        = "DOCKER"
}

resource "docker_image" "traffic-generator" {
    name         = "${var.gcp-region}-docker.pkg.dev/${var.gcp-project}/${google_artifact_registry_repository.repository.repository_id}/traffic-generator"
    keep_locally = false

    build {
        context  = "${path.module}/../../generator/"
        platform = "linux/amd64"
        no_cache = true
    }

    depends_on = [google_artifact_registry_repository.repository]
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
            containers {
                image   = docker_image.traffic-generator.name
                command = ["python", "main.py"]

                args = [
                    "-u", var.generator-user-count,
                    "-l", "http://${module.gce-lb-http.external_ip}/logs"
                ]

                env {
                    name  = "URL"
                    value = google_cloud_run_v2_service.traffic-analyzer.uri
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

    depends_on = [
        docker_registry_image.traffic-generator,
        google_cloud_run_v2_service_iam_member.allow
        ]
}

resource "docker_image" "traffic-analyzer" {
    name         = "${var.gcp-region}-docker.pkg.dev/${var.gcp-project}/${google_artifact_registry_repository.repository.repository_id}/traffic-analyzer"
    keep_locally = false

    build {
        context  = "${path.module}/../../backend/"
        platform = "linux/amd64"
        no_cache = true
    }

    depends_on = [google_artifact_registry_repository.repository]
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
    custom_audiences    = ["http://${module.gce-lb-http.external_ip}"]
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

resource "google_compute_region_network_endpoint_group" "cloudrun-neg" {
    name                  = "cloudrun-neg"
    network_endpoint_type = "SERVERLESS"
    region                = var.gcp-region

    cloud_run {
        service = google_cloud_run_v2_service.traffic-analyzer.name
    }

    lifecycle {
        create_before_destroy = true
    }
}

module "gce-lb-http" {
    source  = "GoogleCloudPlatform/lb-http/google//modules/serverless_negs"
    version = "12.0"
    project = var.gcp-project
    name    = "load-balancer"
    ssl     = false

    backends = {
        default = {
            protocol   = "HTTP"
            enable_cdn = false

            log_config = {
                enable      = true
                sample_rate = 1.0
            }

            groups = [
                {
                    group = google_compute_region_network_endpoint_group.cloudrun-neg.id
                }
            ]
        }
    }
}