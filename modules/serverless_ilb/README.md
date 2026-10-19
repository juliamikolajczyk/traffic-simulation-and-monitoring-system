# Serverless Internal Load Balancer Module
A Serverless HTTP Internal Load Balancer

## Dependency Diagram
![diagram](diagram.png)

<!-- Beginning of terraform docs generated content -->

## Requirements

| Name | Version |
| ---- | ------- |
| <a name="requirement_google"></a> [google](#requirement\_google) | >= 5.0.0 |
| <a name="requirement_google-beta"></a> [google-beta](#requirement\_google-beta) | >= 6.50.0 |

## Providers

| Name | Version |
| ---- | ------- |
| <a name="provider_google"></a> [google](#provider\_google) | >= 5.0.0 |
| <a name="provider_google-beta"></a> [google-beta](#provider\_google-beta) | >= 6.50.0 |

## Modules

No modules.

## Resources

| Name | Type |
| ---- | ---- |
| [google-beta_google_compute_forwarding_rule.forwarding-rule](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_compute_forwarding_rule) | resource |
| [google-beta_google_compute_region_backend_service.backend-service](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_compute_region_backend_service) | resource |
| [google-beta_google_compute_region_target_http_proxy.proxy](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_compute_region_target_http_proxy) | resource |
| [google-beta_google_compute_region_url_map.url-map](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_compute_region_url_map) | resource |
| [google_compute_region_network_endpoint_group.cloudrun-neg](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_region_network_endpoint_group) | resource |

## Inputs

| Name | Description | Type | Default | Required |
| ---- | ----------- | ---- | ------- | :------: |
| <a name="input_cloud-run-service-name"></a> [cloud-run-service-name](#input\_cloud-run-service-name) | name of the Cloud Run Service to pass the traffic to | `string` | n/a | yes |
| <a name="input_gcp-project"></a> [gcp-project](#input\_gcp-project) | your project ID (e.g., my-gcp-project-123) | `string` | n/a | yes |
| <a name="input_gcp-region"></a> [gcp-region](#input\_gcp-region) | the GCP region (e.g., us-central1) | `string` | n/a | yes |
| <a name="input_lb-ip"></a> [lb-ip](#input\_lb-ip) | load balancer's external IP address | `string` | n/a | yes |
| <a name="input_network-id"></a> [network-id](#input\_network-id) | the ID of the network | `string` | n/a | yes |
| <a name="input_proxy-subnetwork-id"></a> [proxy-subnetwork-id](#input\_proxy-subnetwork-id) | the ID of the proxy subnetwork | `string` | n/a | yes |
| <a name="input_subnetwork-id"></a> [subnetwork-id](#input\_subnetwork-id) | the ID of the subnetwork | `string` | n/a | yes |

## Outputs

No outputs.

<!-- End of terraform docs generated content -->