resource "google_project_service" "apis" {
    for_each = toset([
        "artifactregistry.googleapis.com",
        "compute.googleapis.com",
        "run.googleapis.com",
        "redis.googleapis.com",
        "servicenetworking.googleapis.com",
        "cloudresourcemanager.googleapis.com",
        "iam.googleapis.com",
        "appoptimize.googleapis.com",
        "networkmanagement.googleapis.com",
        "dns.googleapis.com"
    ])

    project            = var.gcp-project
    service            = each.key
    disable_on_destroy = false
}

resource "time_sleep" "wait-for-api" {
    create_duration = "30s"

    depends_on = [google_project_service.apis]
}