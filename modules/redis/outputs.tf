output "redis-host" {
    value = google_redis_instance.cache.host
    description = "the IP address of Redis"
}