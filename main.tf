data "google_compute_default_service_account" "default" {}

module "network" {
    source = "./modules/network"

    providers = {
        google      = google
        google-beta = google-beta
    }

    gcp-region  = var.gcp-region
    gcp-project = var.gcp-project

    depends_on = [time_sleep.wait-for-api]
}

module "redis" {
    source = "./modules/redis"

    providers = {
        google      = google
        google-beta = google-beta
    }

    gcp-region        = var.gcp-region
    gcp-project       = var.gcp-project
    network-id        = module.network.network-id
    subnetwork-id     = module.network.subnetwork-id
    ip-range          = module.network.ip-range
    redis-memory-size = var.redis-memory-size

    depends_on = [
        module.network,
        time_sleep.wait-for-api
        ]
}

module "serverless-apps-load-balancer-and-neg" {
    source = "./modules/serverless_apps_load_balancer_and_neg"

    providers = {
        google      = google
        google-beta = google-beta
        docker      = docker
    }

    gcp-region                   = var.gcp-region
    gcp-project                  = var.gcp-project
    network-id                   = module.network.network-id
    subnetwork-id                = module.network.subnetwork-id
    redis-host                   = module.redis.redis-host
    service-account-email        = data.google_compute_default_service_account.default.email
    generator-cpu                = var.generator-cpu
    generator-memory             = var.generator-memory
    generator-task-count         = var.generator-task-count
    generator-parallelism        = var.generator-parallelism
    generator-user-count         = var.generator-user-count
    analyzer-max-instance-count  = var.analyzer-max-instance-count
    analyzer-min-instance-count  = var.analyzer-min-instance-count
    analyzer-cpu                 = var.analyzer-cpu
    analyzer-memory              = var.analyzer-memory

    depends_on = [
        module.redis,
        module.network,
        time_sleep.wait-for-api
    ]
}