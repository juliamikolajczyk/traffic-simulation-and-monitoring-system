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

module "dashboards" {
    source ="./modules/dashboards"

    providers = {
        google = google
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

    depends_on = [module.network]
}

module "traffic-analyzer" {
    source = "./modules/traffic_analyzer"

    providers = {
        google      = google
        google-beta = google-beta
        docker      = docker
    }

    gcp-region                  = var.gcp-region
    gcp-project                 = var.gcp-project
    network-id                  = module.network.network-id
    subnetwork-id               = module.network.subnetwork-id
    redis-host                  = module.redis.redis-host
    service-account-email       = data.google_compute_default_service_account.default.email
    analyzer-max-instance-count = var.analyzer-max-instance-count
    analyzer-min-instance-count = var.analyzer-min-instance-count
    analyzer-cpu                = var.analyzer-cpu
    analyzer-memory             = var.analyzer-memory
    lb-ip                       = module.network.lb-ip

    depends_on = [module.redis]
}

module "serverless-ilb" {
    source = "./modules/serverless_ilb"

        providers = {
        google      = google
        google-beta = google-beta
    }

    gcp-region             = var.gcp-region
    gcp-project            = var.gcp-project
    network-id             = module.network.network-id
    subnetwork-id          = module.network.subnetwork-id 
    proxy-subnetwork-id    = module.network.proxy-subnetwork-id
    lb-ip                  = module.network.lb-ip
    cloud-run-service-name = module.traffic-analyzer.cloud-run-service-name

    depends_on = [module.traffic-analyzer]
}

module "traffic-generator" {
    source = "./modules/traffic_generator"

    providers = {
        google      = google
        google-beta = google-beta
        docker      = docker
    }

    gcp-region            = var.gcp-region
    gcp-project           = var.gcp-project
    network-id            = module.network.network-id
    subnetwork-id         = module.network.subnetwork-id
    generator-cpu         = var.generator-cpu
    generator-memory      = var.generator-memory
    generator-task-count  = var.generator-task-count
    generator-parallelism = var.generator-parallelism
    generator-user-count  = var.generator-user-count
    exec-time             = var.exec-time
    lb-ip                 = module.network.lb-ip
    gcp-repository        = module.traffic-analyzer.gcp-repository
    analyzer-uri          = module.traffic-analyzer.analyzer-uri

    depends_on = [module.serverless-ilb]
}