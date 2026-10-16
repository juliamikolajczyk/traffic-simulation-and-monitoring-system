output "network-id" {
    value       = google_compute_network.vpc-network.id
    description = "the ID of the network"
}

output "subnetwork-id" {
    value       = google_compute_subnetwork.vpc-subnetwork.id
    description = "the ID of the subnetwork"
}

output "ip-range" {
    value       = google_compute_global_address.private-ip.name
    description = "the name of the allocated internal IP range reserved for VPC peering"
}

output "proxy-subnetwork-id" {
    value       = google_compute_subnetwork.proxy-subnetwork.id
    description = "the ID of the proxy subnetwork"
}

output "lb-ip" {
    value       = google_compute_address.lb-ip.address
    description = "load balancer's external IP address"
}