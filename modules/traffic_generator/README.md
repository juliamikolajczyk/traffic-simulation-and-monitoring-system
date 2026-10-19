# Traffic generator
A module deploying the [generator app](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/generator) into the GCP cloud as a scalable Cloud Run Job.

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
| <a name="provider_google-beta"></a> [google-beta](#provider\_google-beta) | >= 6.50.0 |

## Modules

No modules.

## Resources

| Name | Type |
| ---- | ---- |
| [docker_image.traffic-generator](https://registry.terraform.io/providers/kreuzwerker/docker/4.5.0/docs/resources/image) | resource |
| [docker_registry_image.traffic-generator](https://registry.terraform.io/providers/kreuzwerker/docker/4.5.0/docs/resources/registry_image) | resource |
| [google-beta_google_cloud_run_v2_job.traffic-generator](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_cloud_run_v2_job) | resource |

## Inputs

| Name | Description | Type | Default | Required |
| ---- | ----------- | ---- | ------- | :------: |
| <a name="input_analyzer-uri"></a> [analyzer-uri](#input\_analyzer-uri) | traffic analyzer's URI | `string` | n/a | yes |
| <a name="input_exec-time"></a> [exec-time](#input\_exec-time) | for how many seconds the traffic is generated (e.g., 3400); must be less than or equal to 604715 | `number` | `600` | no |
| <a name="input_gcp-project"></a> [gcp-project](#input\_gcp-project) | your project ID (e.g., my-gcp-project-123) | `string` | n/a | yes |
| <a name="input_gcp-region"></a> [gcp-region](#input\_gcp-region) | the GCP region (e.g., us-central1) | `string` | n/a | yes |
| <a name="input_gcp-repository"></a> [gcp-repository](#input\_gcp-repository) | the ID of the registry repository | `string` | n/a | yes |
| <a name="input_generator-cpu"></a> [generator-cpu](#input\_generator-cpu) | the number of CPU cores allocated to each generator instance | `string` | `"2"` | no |
| <a name="input_generator-memory"></a> [generator-memory](#input\_generator-memory) | the amount of RAM allocated to each generator instance | `string` | `"2Gi"` | no |
| <a name="input_generator-parallelism"></a> [generator-parallelism](#input\_generator-parallelism) | the maximum number of tasks that can be run at the exact same time | `number` | `10` | no |
| <a name="input_generator-task-count"></a> [generator-task-count](#input\_generator-task-count) | the total number of generator instances that need to be run to complete the job | `number` | `5` | no |
| <a name="input_generator-user-count"></a> [generator-user-count](#input\_generator-user-count) | the number of users generating traffic from an instance | `string` | `"5"` | no |
| <a name="input_lb-ip"></a> [lb-ip](#input\_lb-ip) | load balancer's external IP address | `string` | n/a | yes |
| <a name="input_network-id"></a> [network-id](#input\_network-id) | the ID of the network | `string` | n/a | yes |
| <a name="input_subnetwork-id"></a> [subnetwork-id](#input\_subnetwork-id) | the ID of the subnetwork | `string` | n/a | yes |

## Outputs

No outputs.

<!-- End of terraform docs generated content -->