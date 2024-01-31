terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.14.0"
    }
  }
}

provider "google" {
  credentials = "./keys/cred.json"
  project     = "terraform-demo-412813"
  region      = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-demo-412813-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}