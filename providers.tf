terraform {
    backend "gcs" {} 
    //first, create GCS via console, then, in the terminal, 
    //run terraform init -backend-config="bucket=<YOUR_BUCKET_ID>" -backend-config="prefix=<TERRAFORM_STARTING_POINT>"
    
    required_providers {
        google = {
            source  = "hashicorp/google"
            version = ">= 5.0.0"
        }

        google-beta = {
            source  = "hashicorp/google-beta"
            version = ">= 6.50.0"
        }

        docker = {
            source  = "kreuzwerker/docker"
            version = "4.5.0"
        }

        time = {
            source  = "hashicorp/time"
            version = "0.14.1"
        }
    }
}

provider "google" {
    project = var.gcp-project
    region  = var.gcp-region
}

provider "google-beta" {
    project = var.gcp-project
    region  = var.gcp-region
}

provider "docker" {
    registry_auth {
        address  = "${var.gcp-region}-docker.pkg.dev"
        username = "oauth2accesstoken"
        password = data.google_client_config.default.access_token
    }
}

data "google_client_config" "default" {}