# Redis Instance Module

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

## Modules

No modules.

## Resources

| Name | Type |
| ---- | ---- |
| [google_redis_instance.cache](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/redis_instance) | resource |

## Inputs

| Name | Description | Type | Default | Required |
| ---- | ----------- | ---- | ------- | :------: |
| <a name="input_gcp-project"></a> [gcp-project](#input\_gcp-project) | your project ID (e.g., my-gcp-project-123) | `string` | n/a | yes |
| <a name="input_gcp-region"></a> [gcp-region](#input\_gcp-region) | the GCP region (e.g., us-central1) | `string` | n/a | yes |
| <a name="input_ip-range"></a> [ip-range](#input\_ip-range) | the name of the allocated internal IP range reserved for VPC peering | `string` | n/a | yes |
| <a name="input_network-id"></a> [network-id](#input\_network-id) | the ID of the network | `string` | n/a | yes |
| <a name="input_redis-memory-size"></a> [redis-memory-size](#input\_redis-memory-size) | the amount of RAM for Redis | `number` | `2` | no |
| <a name="input_subnetwork-id"></a> [subnetwork-id](#input\_subnetwork-id) | the ID of the subnetwork | `string` | n/a | yes |

## Outputs

| Name | Description |
| ---- | ----------- |
| <a name="output_redis-host"></a> [redis-host](#output\_redis-host) | the IP address of Redis |

<!-- End of terraform docs generated content -->