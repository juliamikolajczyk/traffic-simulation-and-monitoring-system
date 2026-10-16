resource "google_logging_metric" "normal-traffic" {
  name   = "normal-traffic"
  filter = "textPayload=~\"a request\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    unit        = "1"
    display_name = "Normal"
  }
}

resource "google_logging_metric" "error-401" {
  name   = "401"
  filter = "textPayload=~\"a 401 request\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    unit        = "1"
    display_name = "401"
  }
}

resource "google_logging_metric" "error-404" {
  name   = "404"
  filter = "textPayload=~\"a 404 request\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    unit        = "1"
    display_name = "404"
  }
}

resource "google_logging_metric" "dos" {
  name   = "dos"
  filter = "textPayload=~\"DOS\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    unit        = "1"
    display_name = "DOS"
  }
}

resource "google_logging_metric" "non-existing-operation" {
  name   = "non-existing-operation-tester"
  filter = "textPayload=~\"non-existing operation tester\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    unit        = "1"
    display_name = "non-existing-operation tester"
  }
}

resource "google_logging_metric" "brute-force" {
  name   = "brute-force"
  filter = "textPayload=~\"brute force\""
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    unit        = "1"
    display_name = "brute-force"
  }
}

resource "google_monitoring_dashboard" "attacks" {
    project = var.gcp-project
    dashboard_json = templatefile("${path.module}/dashboards/three-metrics-linear-template.json.tftpl",{
        display-name = "Attacks"
        title        = "Attacks"
        metric1      = google_logging_metric.dos.name
        metric1-name = "DOS"
        metric2      = google_logging_metric.brute-force.name
        metric2-name = "brute force"
        metric3      = google_logging_metric.non-existing-operation.name
        metric3-name = "non-existing operation tester"

    })
}

resource "google_monitoring_dashboard" "traffic-types" {
    project = var.gcp-project
    dashboard_json = templatefile("${path.module}/dashboards/three-metrics-linear-template.json.tftpl",{
        display-name = "Traffic types"
        title        = "Traffic types"
        metric1      = google_logging_metric.normal-traffic.name
        metric1-name = "other"
        metric2      = google_logging_metric.error-401.name
        metric2-name = "401"
        metric3      = google_logging_metric.error-404.name
        metric3-name = "404"

    })
}

resource "google_monitoring_dashboard" "traffic-analyzer-latency" {
    project = var.gcp-project
    dashboard_json = templatefile("${path.module}/dashboards/traffic-analyzer-latency.json",{})
}