<div align="center">

# Traffic Simulation and Monitoring System

[![](https://img.shields.io/badge/Python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![](https://img.shields.io/badge/FastAPI-0.141.1-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![](https://img.shields.io/badge/Redis-8.1.0-dc382d.svg?logo=redis&logoColor=white)](https://redis.io/)
[![](https://img.shields.io/badge/Terraform-1.16+-844FBA.svg?logo=terraform&logoColor=white)](https://www.terraform.io/)

A system designed to simulate realistic behavior of concurrent users and monitor it, implemented using asynchronous Python code bypassing the GIL and six Terraform modules with Redis as the "brain". Deployed via Google Cloud Platform.
</div>

An example log:
```json
{
  "timestampMs": 1788205868908,
  "accountId": "81ff4f2f7b2773b2f7af9cef2b7cd3e7",
  "ip": "25.151.149.188",
  "operation": "ViewCatalog",
  "method": "GET",
  "status": "200",
  "message": "OK",
  "userAgent": "Brave"
}
```
Example dashboards:

<img width="370" height="215.3" alt="image" src="https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/blob/docs/traffic_types_dashboard.png" /> <img width="370" height="215.3" alt="image" src="https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/blob/docs/attacks_dashboard.png" />



## Features:
- a <b> [network](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/modules/network) </b> module with VPC Network, VPC Subnetwork, Proxy Subnetwork and more,
- a <b> [dashboards](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/modules/dashboards) </b> module featuring among others a <b> [template for a custom linear type dashboard](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/blob/main/modules/dashboards/dashboards/three-metrics-linear-template.json.tftpl) </b> with three metrics,
- a <b> [serverless_ilb](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/modules/serverless_ilb) </b> module including a <b> serverless internal load balancer </b> to route the traffic,
- a <b> [generator app](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/generator) </b> implemented via <b> asynchronous Python </b> code, where the user's next operation is a <b> dynamically weighted choice </b> and the <b> attacks </b> (such as DDOS, brute-force, non-existing operation tester) are <b> injected randomly</b>,
- a <b> [traffic_generator](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/modules/traffic_generator) </b> module, which deploys the <b> [generator app](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/generator) </b> into the <b> cloud </b> - it can be <b> scaled </b> both <b> horizontally </b> and <b> vertically</b>, the number of users and the duration of the simulation are <b> customizable</b>, all based on variable values provided
- a <b> [backend app](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/backend)</b>, which <b> processes logs </b> and <b> flags </b> the incoming traffic accordingly based on a <b> 10 seconds time window</b>, using a <b> [Redis](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/modules/redis) </b> instance as the brain
- a both <b> horizontally </b> and <b> vertically scalable [traffic_analyzer](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/modules/traffic_analyzer) </b> module, whose job is running the <b> [backend](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/tree/main/backend) </b> in the <b> cloud</b>

## Quick Start
### Prerequisites:
- a [GCP](https://cloud.google.com) account with a [Google Cloud Storage](https://console.cloud.google.com/storage/) instance deployed
- a [GCP service account](https://console.cloud.google.com/iam-admin/serviceaccounts) to control the Traffic Simulation and Monitoring System deployment process (via terraform commands), the "Owner" IAM role should be more than enough
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [Docker](https://docs.docker.com/get-started/get-docker/)


1. Open the project folder via terminal, make sure you are logged in your GCP service account in it.
2. Create and save a terraform.tfvars file if you don't have one already, using this template:
```hcl
gcp-project                  = "your-project-id"
gcp-region                   = "your-region"
generator-cpu                = "2"
generator-memory             = "2Gi"
generator-task-count         = 5
generator-parallelism        = 10
generator-user-count         = "5000"
analyzer-max-instance-count  = 10
analyzer-min-instance-count  = 1
analyzer-cpu                 = "2"
analyzer-memory              = "2Gi"
exec-time                    = 1200
```
3. Find your GCS bucket's ID. Run this command inside the terminal:
```bash
terraform init -backend-config="bucket=<YOUR_BUCKET_ID>" -backend-config="prefix=<TERRAFORM_STARTING_POINT>"
```
4. Run these commands inside the terminal:
```bash
terraform plan
```
```bash
terraform apply
```
5. Follow the instructions inside the terminal.
6. After a while, the project should be running. Once you stop using it, to avoid unnecessary billing, run this command:
```bash
terraform destroy
```
7. You can deploy the project again. In order to do this, follow steps 1-6.

## Community
For questions, ideas, etc., use [GitHub Discussions](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/discussions). Issues and pull requests are welcome.

## Team

| Name | Role |
| --------------- | ----------- |
| [Julia Mikołajczyk](https://github.com/juliamikolajczyk) | Project Lead, Cloud Architect <br>and DevOps Engineer |
| [PRO100KatYT](https://github.com/PRO100KatYT) | App Developer |

## License
Released under the [Apache 2.0 License](https://github.com/juliamikolajczyk/traffic-simulation-and-monitoring-system/main/LICENSE)
