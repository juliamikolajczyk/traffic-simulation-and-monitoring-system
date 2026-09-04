resource "google_compute_region_network_endpoint_group" "cloudrun-neg" {
    name                  = "cloudrun-neg"
    network_endpoint_type = "SERVERLESS"
    region                = var.gcp-region

    cloud_run {
        service = var.cloud-run-service-name
    }

    lifecycle {
        create_before_destroy = true
    }
}

resource "google_compute_region_backend_service" "backend-service" {
  name                  = "backend-service"
  provider              = google-beta
  region                = var.gcp-region
  protocol              = "HTTP"
  load_balancing_scheme = "INTERNAL_MANAGED"

  backend {
    group = google_compute_region_network_endpoint_group.cloudrun-neg.id
  }
}

resource "google_compute_region_url_map" "url-map" {
  name            = "url-map"
  provider        = google-beta
  region          = var.gcp-region
  default_service = google_compute_region_backend_service.backend-service.id
}

resource "google_compute_region_target_http_proxy" "proxy" {
  name     = "proxy"
  provider = google-beta
  region   = var.gcp-region
  url_map  = google_compute_region_url_map.url-map.id
}

resource "google_compute_forwarding_rule" "forwarding-rule" {
  name                  = "forwarding-rule"
  provider              = google-beta
  region                = var.gcp-region
  ip_protocol           = "TCP"
  load_balancing_scheme = "INTERNAL_MANAGED"
  port_range            = "80"
  target                = google_compute_region_target_http_proxy.proxy.id
  network               = var.network-id
  subnetwork            = var.subnetwork-id
  network_tier          = "PREMIUM"
  ip_address            = var.lb-ip
}