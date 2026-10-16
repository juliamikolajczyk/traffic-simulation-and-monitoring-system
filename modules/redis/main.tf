resource "google_redis_instance" "cache" {
    name           = "cache"
    tier           = "STANDARD_HA"
    memory_size_gb = var.redis-memory-size

    location_id             = "${var.gcp-region}-a"
    alternative_location_id = "${var.gcp-region}-f"

    authorized_network = var.network-id
    connect_mode       = "PRIVATE_SERVICE_ACCESS"

    redis_version     = "REDIS_7_2"
    display_name      = "redis"
    reserved_ip_range = var.ip-range

    timeouts {
        create = "45m"
        update = "45m"
        delete = "45m"
    }

    maintenance_policy {
        weekly_maintenance_window {
            day = "TUESDAY"
            start_time {
                hours   = 0
                minutes = 30
                seconds = 0
                nanos   = 0
            }
        }
    }

    lifecycle {
        prevent_destroy = false
    }
}