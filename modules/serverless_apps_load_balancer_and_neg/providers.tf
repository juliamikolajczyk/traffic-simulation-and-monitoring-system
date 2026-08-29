terraform {
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
    }
}