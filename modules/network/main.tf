resource "google_compute_network" "vpc-network" {
    name                    = "vpc-network"
    auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "vpc-subnetwork" {
    name                     = "vpc-subnetwork"
    ip_cidr_range            = "10.0.0.0/24"
    region                   = var.gcp-region
    network                  = google_compute_network.vpc-network.id
    private_ip_google_access = true
}

resource "google_compute_global_address" "private-ip" {
    name          = "private-ip"
    purpose       = "VPC_PEERING"
    address_type  = "INTERNAL"
    prefix_length = 16
    network       = google_compute_network.vpc-network.id
}

resource "google_service_networking_connection" "private-vpc" {
    network                 = google_compute_network.vpc-network.id
    service                 = "servicenetworking.googleapis.com"
    reserved_peering_ranges = [google_compute_global_address.private-ip.name]
}