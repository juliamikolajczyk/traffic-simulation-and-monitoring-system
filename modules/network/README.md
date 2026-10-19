# Network Module
A Network Module, including VPC Network, VPC Subnetwork, Proxy Subnetwork, Load Balancer's IP and more.

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
| [google-beta_google_compute_subnetwork.proxy-subnetwork](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_compute_subnetwork) | resource |
| [google_compute_address.lb-ip](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_address) | resource |
| [google_compute_global_address.private-ip](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_global_address) | resource |
| [google_compute_network.vpc-network](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_network) | resource |
| [google_compute_subnetwork.vpc-subnetwork](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_subnetwork) | resource |
| [google_service_networking_connection.private-vpc](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/service_networking_connection) | resource |

## Inputs

| Name | Description | Type | Default | Required |
| ---- | ----------- | ---- | ------- | :------: |
| <a name="input_gcp-project"></a> [gcp-project](#input\_gcp-project) | your project ID (e.g., my-gcp-project-123) | `string` | n/a | yes |
| <a name="input_gcp-region"></a> [gcp-region](#input\_gcp-region) | the GCP region (e.g., us-central1) | `string` | n/a | yes |

## Outputs

| Name | Description |
| ---- | ----------- |
| <a name="output_ip-range"></a> [ip-range](#output\_ip-range) | the name of the allocated internal IP range reserved for VPC peering |
| <a name="output_lb-ip"></a> [lb-ip](#output\_lb-ip) | load balancer's external IP address |
| <a name="output_network-id"></a> [network-id](#output\_network-id) | the ID of the network |
| <a name="output_proxy-subnetwork-id"></a> [proxy-subnetwork-id](#output\_proxy-subnetwork-id) | the ID of the proxy subnetwork |
| <a name="output_subnetwork-id"></a> [subnetwork-id](#output\_subnetwork-id) | the ID of the subnetwork |

<!-- End of terraform docs generated content -->