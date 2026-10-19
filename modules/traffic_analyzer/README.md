# Traffic analyzer

A module deploying the [backend app](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/backend) into the GCP cloud as a scalable Cloud Run Service.

## Dependency Diagram
![diagram](diagram.png)

<!-- Beginning of terraform docs generated content -->

## Requirements

| Name | Version |
| ---- | ------- |
| <a name="requirement_docker"></a> [docker](#requirement\_docker) | 4.5.0 |
| <a name="requirement_google"></a> [google](#requirement\_google) | >= 5.0.0 |
| <a name="requirement_google-beta"></a> [google-beta](#requirement\_google-beta) | >= 6.50.0 |

## Providers

| Name | Version |
| ---- | ------- |
| <a name="provider_docker"></a> [docker](#provider\_docker) | 4.5.0 |
| <a name="provider_google"></a> [google](#provider\_google) | >= 5.0.0 |
| <a name="provider_google-beta"></a> [google-beta](#provider\_google-beta) | >= 6.50.0 |

## Modules

No modules.

## Resources

| Name | Type |
| ---- | ---- |
| [docker_image.traffic-analyzer](https://registry.terraform.io/providers/kreuzwerker/docker/4.5.0/docs/resources/image) | resource |
| [docker_registry_image.traffic-analyzer](https://registry.terraform.io/providers/kreuzwerker/docker/4.5.0/docs/resources/registry_image) | resource |
| [google-beta_google_cloud_run_v2_service.traffic-analyzer](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_cloud_run_v2_service) | resource |
| [google_artifact_registry_repository.repository](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/artifact_registry_repository) | resource |
| [google_cloud_run_v2_service_iam_member.allow](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_run_v2_service_iam_member) | resource |

## Inputs

| Name | Description | Type | Default | Required |
| ---- | ----------- | ---- | ------- | :------: |
| <a name="input_analyzer-cpu"></a> [analyzer-cpu](#input\_analyzer-cpu) | the number of CPU cores allocated to each analyzer instance | `string` | `"2"` | no |
| <a name="input_analyzer-max-instance-count"></a> [analyzer-max-instance-count](#input\_analyzer-max-instance-count) | the maximum number of analyzer instances | `number` | `10` | no |
| <a name="input_analyzer-memory"></a> [analyzer-memory](#input\_analyzer-memory) | the amount of RAM allocated to each analyzer instance | `string` | `"2Gi"` | no |
| <a name="input_analyzer-min-instance-count"></a> [analyzer-min-instance-count](#input\_analyzer-min-instance-count) | the minimum number of analyzer instances | `number` | `1` | no |
| <a name="input_gcp-project"></a> [gcp-project](#input\_gcp-project) | your project ID (e.g., my-gcp-project-123) | `string` | n/a | yes |
| <a name="input_gcp-region"></a> [gcp-region](#input\_gcp-region) | the GCP region (e.g., us-central1) | `string` | n/a | yes |
| <a name="input_lb-ip"></a> [lb-ip](#input\_lb-ip) | load balancer's external IP address | `string` | n/a | yes |
| <a name="input_network-id"></a> [network-id](#input\_network-id) | the ID of the network | `string` | n/a | yes |
| <a name="input_redis-host"></a> [redis-host](#input\_redis-host) | the IP address of Redis | `string` | n/a | yes |
| <a name="input_service-account-email"></a> [service-account-email](#input\_service-account-email) | the email address of the service account | `string` | n/a | yes |
| <a name="input_subnetwork-id"></a> [subnetwork-id](#input\_subnetwork-id) | the ID of the subnetwork | `string` | n/a | yes |

## Outputs

| Name | Description |
| ---- | ----------- |
| <a name="output_analyzer-uri"></a> [analyzer-uri](#output\_analyzer-uri) | traffic analyzer's URI |
| <a name="output_cloud-run-service-name"></a> [cloud-run-service-name](#output\_cloud-run-service-name) | name of the Cloud Run Service to pass the traffic to |
| <a name="output_gcp-repository"></a> [gcp-repository](#output\_gcp-repository) | the ID of the registry repository |

<!-- End of terraform docs generated content -->