output "cloud-run-service-name" {
    value       = google_cloud_run_v2_service.traffic-analyzer.name
    description = "name of the Cloud Run Service to pass the traffic to"
}

output "gcp-repository" {
    value       = google_artifact_registry_repository.repository.repository_id
    description = "the ID of the registry repository"
}

output "analyzer-uri" {
    value       = google_cloud_run_v2_service.traffic-analyzer.uri
    description = "traffic analyzer's URI"
}